from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from services import runtime_settings
from config import settings

router = APIRouter(prefix="/api/admin/settings", tags=["AdminSettings"])


class PromptLimitPayload(BaseModel):
    MAX_PROMPT_CHARS: Optional[int]


@router.get("/")
def get_prompt_limit():
    """Devuelve el valor actual del límite de caracteres del prompt (override runtime o config)"""
    override = runtime_settings.get_max_prompt_chars()
    value = override if override is not None else settings.MAX_PROMPT_CHARS
    return {"MAX_PROMPT_CHARS": int(value)}


@router.put("/")
def set_prompt_limit(payload: PromptLimitPayload):
    """Establece un override runtime para MAX_PROMPT_CHARS. Si el valor es null, se resetea al valor de config."""
    if payload.MAX_PROMPT_CHARS is None:
        runtime_settings.set_max_prompt_chars(None)
        return {"MAX_PROMPT_CHARS": int(settings.MAX_PROMPT_CHARS), "note": "reset to config"}

    if payload.MAX_PROMPT_CHARS <= 0:
        raise HTTPException(status_code=400, detail="MAX_PROMPT_CHARS must be a positive integer")

    # Aplicar override en memoria
    runtime_settings.set_max_prompt_chars(payload.MAX_PROMPT_CHARS)
    return {"MAX_PROMPT_CHARS": int(payload.MAX_PROMPT_CHARS), "note": "runtime override"}
