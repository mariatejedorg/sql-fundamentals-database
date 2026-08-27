"""Crea el esquema SQLite y carga los datos de empresas y precios."""

import sqlite3
from pathlib import Path

import pandas as pd

DB_DIR = Path(__file__).resolve().parent.parent / "db"
SCHEMA_PATH = DB_DIR / "schema.sql"
DB_PATH = DB_DIR / "fundamentales.db"


def build_database(empresas: pd.DataFrame, precios: pd.DataFrame) -> Path:
    """Crea (o recrea) la base de datos SQLite a partir del esquema y los DataFrames."""
    DB_PATH.unlink(missing_ok=True)

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        empresas.to_sql("empresas", conn, if_exists="append", index=False)
        precios.to_sql("precios_historicos", conn, if_exists="append", index=False)
        conn.commit()
    finally:
        conn.close()

    return DB_PATH
