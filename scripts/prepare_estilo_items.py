#!/usr/bin/env python3
"""Script ligero para validar fragments JSON y generar SQL/JSON de importación

Uso:
  python scripts/prepare_estilo_items.py --input estilos/cleaned/MANUAL_DE_ESTILO__FRAGMENTS.json

El script valida el esquema mínimo y, en modo dry-run, imprime INSERTs SQL
o un fixture JSON listo para importar. No hace writes a la base de datos por defecto.
"""
import argparse
import json
from pathlib import Path


def validate_fragment(f):
    required = {"id", "titulo", "tipo", "orden", "texto"}
    missing = required - set(f.keys())
    if missing:
        raise ValueError(f"Fragment {f.get('id','<no-id>')} missing keys: {missing}")


def generate_sql(fragments):
    lines = []
    for f in fragments:
        text = f['texto'].replace("'", "''")
        lines.append(
            "INSERT INTO estilo_item (id, titulo, tipo, orden, texto) VALUES ('{id}', '{titulo}', '{tipo}', {orden}, '{texto}');""".format(
                id=f['id'], titulo=f['titulo'][:100].replace("'", "''"), tipo=f['tipo'], orden=int(f['orden']), texto=text[:1000]
            )
        )
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, help="Fragments JSON")
    p.add_argument("--out-sql", help="Write SQL to this file")
    p.add_argument("--out-json", help="Write normalized JSON to this file")
    p.add_argument("--dry-run", action="store_true", default=True, dest="dry_run",
                   help="Dry run (default): print summary and do not write DB)")
    args = p.parse_args()

    path = Path(args.input)
    if not path.exists():
        print(f"Input file not found: {path}")
        return 2

    fragments = json.loads(path.read_text(encoding="utf-8"))
    for f in fragments:
        validate_fragment(f)

    print(f"Validated {len(fragments)} fragments from {path}")

    if args.out_json:
        outp = Path(args.out_json)
        outp.write_text(json.dumps(fragments, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote normalized JSON to {outp}")

    sql = generate_sql(fragments)
    if args.out_sql:
        Path(args.out_sql).write_text(sql, encoding="utf-8")
        print(f"Wrote SQL to {args.out_sql}")

    if args.dry_run:
        print("-- dry-run -- sample SQL (first 5 INSERTs):\n")
        print('\n'.join(sql.splitlines()[:5]))


if __name__ == '__main__':
    main()
