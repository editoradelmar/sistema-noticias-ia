"""
Router para extracción de texto desde archivos (PDF, DOCX, DOC, TXT)

Endpoint: POST /api/files/extract

Esta implementación intenta usar bibliotecas Python cuando están disponibles:
- PDF: PyMuPDF (fitz)
- DOCX: python-docx
- DOC (antiguo): intenta convertir usando LibreOffice (soffice) a DOCX y luego parsear
- OCR (opcional): pytesseract + Pillow (si está instalado y Tesseract disponible)

La ruta devuelve JSON: { success, title, content, ocr_used, warnings }
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from typing import List
import tempfile
import os
import shutil
import subprocess

router = APIRouter()

# Intentar importaciones opcionales
try:
    import fitz  # PyMuPDF
except Exception:
    fitz = None

try:
    import docx
except Exception:
    docx = None

try:
    import filetype
except Exception:
    filetype = None

try:
    from PIL import Image
    import pytesseract
except Exception:
    Image = None
    pytesseract = None


def smart_title_from_text(text: str) -> str:
    if not text:
        return ''
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if not lines:
        return ''
    first = lines[0]
    if 10 <= len(first) <= 200:
        return first
    # buscar en primeras 3 líneas
    for l in lines[:3]:
        if 10 < len(l) < 200:
            return l
    return first[:200]


def extract_text_pdf(path: str) -> (str, List[str], bool):
    warnings = []
    ocr_used = False
    if not fitz:
        raise RuntimeError('PyMuPDF (fitz) no está instalado en el servidor')
    try:
        doc = fitz.open(path)
        text = ''
        for page in doc:
            text += page.get_text('text') + '\n'
        text = text.strip()
        if not text and pytesseract and Image:
            # intentar OCR renderizando páginas
            ocr_used = True
            ocr_text = ''
            for i in range(doc.page_count):
                pix = doc.load_page(i).get_pixmap(dpi=200)
                img = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
                ocr_text += pytesseract.image_to_string(img, lang='eng+spa') + '\n'
            text = ocr_text.strip()
            if not text:
                warnings.append('No se extrajo texto incluso con OCR')
        doc.close()
        return text, warnings, ocr_used
    except Exception as e:
        raise RuntimeError(f'Error extrayendo PDF: {e}')


def extract_text_docx(path: str) -> (str, List[str]):
    warnings = []
    if not docx:
        raise RuntimeError('python-docx no está instalado en el servidor')
    try:
        document = docx.Document(path)
        paragraphs = [p.text for p in document.paragraphs if p.text and p.text.strip()]
        text = '\n'.join(paragraphs)
        return text.strip(), warnings
    except Exception as e:
        raise RuntimeError(f'Error extrayendo DOCX: {e}')


def convert_doc_to_docx(path: str, tmpdir: str) -> str:
    # Usa LibreOffice (soffice) para convertir .doc -> .docx
    # Retorna ruta del nuevo archivo .docx
    soffice = shutil.which('soffice') or shutil.which('libreoffice')
    if not soffice:
        raise RuntimeError('LibreOffice (soffice) no está disponible para convertir .doc a .docx')
    try:
        subprocess.run([
            soffice,
            '--headless',
            '--convert-to', 'docx',
            '--outdir', tmpdir,
            path
        ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        base = os.path.basename(path)
        name, _ = os.path.splitext(base)
        out_path = os.path.join(tmpdir, f'{name}.docx')
        if not os.path.exists(out_path):
            raise RuntimeError('Conversión a docx no produjo el archivo esperado')
        return out_path
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f'Error en conversión con LibreOffice: {e.stderr.decode(errors="ignore")}')


@router.post('/extract')
async def extract_file(file: UploadFile = File(...)):
    """Extrae texto del archivo subido y devuelve title/content/ocr_used/warnings"""
    # Guardar en temp
    suffix = os.path.splitext(file.filename or '')[1].lower()
    tmpdir = tempfile.mkdtemp(prefix='file_extract_')
    tmp_path = os.path.join(tmpdir, f'upload{suffix}')
    try:
        contents = await file.read()
        with open(tmp_path, 'wb') as f:
            f.write(contents)

        # Detección de tipo preferente
        kind = None
        if filetype:
            try:
                kt = filetype.guess(contents)
                if kt:
                    kind = kt.mime
            except Exception:
                kind = None

        content_type = file.content_type or kind or ''

        # Ramas de extracción
        if content_type.startswith('text') or suffix == '.txt':
            try:
                text = contents.decode('utf-8', errors='replace')
            except Exception:
                text = contents.decode('latin-1', errors='replace')
            title = smart_title_from_text(text)
            return { 'success': True, 'title': title, 'content': text, 'ocr_used': False, 'warnings': [] }

        if 'pdf' in content_type or suffix == '.pdf':
            try:
                text, warnings, ocr_used = extract_text_pdf(tmp_path)
                title = smart_title_from_text(text)
                return { 'success': True, 'title': title, 'content': text, 'ocr_used': ocr_used, 'warnings': warnings }
            except RuntimeError as e:
                raise HTTPException(status_code=500, detail=str(e))

        if 'officedocument.wordprocessingml.document' in content_type or suffix == '.docx':
            try:
                text, warnings = extract_text_docx(tmp_path)
                title = smart_title_from_text(text)
                return { 'success': True, 'title': title, 'content': text, 'ocr_used': False, 'warnings': warnings }
            except RuntimeError as e:
                raise HTTPException(status_code=500, detail=str(e))

        if suffix == '.doc' or 'msword' in content_type:
            # intentar convertir a docx
            try:
                converted = convert_doc_to_docx(tmp_path, tmpdir)
                text, warnings = extract_text_docx(converted)
                title = smart_title_from_text(text)
                return { 'success': True, 'title': title, 'content': text, 'ocr_used': False, 'warnings': warnings }
            except RuntimeError as e:
                raise HTTPException(status_code=500, detail=str(e))

        # Si no sabemos cómo tratarlo
        raise HTTPException(status_code=415, detail='Formato no soportado para extracción')
    finally:
        try:
            shutil.rmtree(tmpdir)
        except Exception:
            pass
