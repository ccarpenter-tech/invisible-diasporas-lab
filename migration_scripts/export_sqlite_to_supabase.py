import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "diaspora_asian_media.sqlite"
OUT_DIR = BASE_DIR / "supabase_import"

TABLES = [
    "articles",
    "migration_destination",
    "migration_origin",
]

OUT_DIR.mkdir(exist_ok=True)

def sqlite_type_to_postgres(col_name, sqlite_type):
    name = col_name.lower()
    sqlite_type = (sqlite_type or "").upper()

    if name in ["date"]:
        return "text"

    if "year" in name:
        return "integer"

    if any(word in name for word in ["tone", "score", "index", "share", "stock", "count", "population", "total"]):
        return "double precision"

    if "INT" in sqlite_type:
        return "integer"

    if any(t in sqlite_type for t in ["REAL", "FLOA", "DOUB", "NUM"]):
        return "double precision"

    return "text"

def quote_ident(name):
    return '"' + name.replace('"', '""') + '"'

conn = sqlite3.connect(DB_PATH)

schema_lines = []

for table in TABLES:
    print(f"Exportando tabela: {table}")

    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    csv_path = OUT_DIR / f"{table}.csv"
    df.to_csv(csv_path, index=False)

    columns_info = conn.execute(f"PRAGMA table_info({table})").fetchall()

    schema_lines.append(f"drop table if exists public.{quote_ident(table)} cascade;")
    schema_lines.append(f"create table public.{quote_ident(table)} (")

    column_defs = []
    for col in columns_info:
        col_name = col[1]
        sqlite_type = col[2]
        pg_type = sqlite_type_to_postgres(col_name, sqlite_type)
        column_defs.append(f"  {quote_ident(col_name)} {pg_type}")

    schema_lines.append(",\n".join(column_defs))
    schema_lines.append(");")
    schema_lines.append("")

    schema_lines.append(f"alter table public.{quote_ident(table)} enable row level security;")
    schema_lines.append(
        f'create policy "public can read {table}" on public.{quote_ident(table)} '
        f"for select to anon using (true);"
    )
    schema_lines.append("")

conn.close()

schema_path = OUT_DIR / "schema_core.sql"
schema_path.write_text("\n".join(schema_lines), encoding="utf-8")

print("")
print("Pronto!")
print(f"CSVs exportados em: {OUT_DIR}")
print(f"SQL gerado em: {schema_path}")