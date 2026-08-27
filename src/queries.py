"""Ejecuta las consultas SQL documentadas en sql/ y devuelve resultado + objetivo de negocio."""

import sqlite3
from pathlib import Path

import pandas as pd

SQL_DIR = Path(__file__).resolve().parent.parent / "sql"

QUERY_FILES = [
    "01_ranking_per_por_sector.sql",
    "02_mejor_margen_por_sector.sql",
    "03_evolucion_metrica_por_sector.sql",
    "04_rentabilidad_reciente_por_empresa.sql",
]


def _business_objective(sql_text: str) -> str:
    """Extrae el objetivo de negocio de las líneas de comentario iniciales del .sql,
    para no duplicar la documentación en Python."""
    lines = []
    for line in sql_text.splitlines():
        if not line.startswith("--"):
            break
        lines.append(line.removeprefix("--").strip())
    return " ".join(lines)


def run_query(conn: sqlite3.Connection, filename: str) -> tuple[str, pd.DataFrame]:
    sql_text = (SQL_DIR / filename).read_text(encoding="utf-8")
    objective = _business_objective(sql_text)
    result = pd.read_sql_query(sql_text, conn)
    return objective, result


def run_all_queries(db_path: Path) -> list[dict]:
    conn = sqlite3.connect(db_path)
    try:
        results = []
        for filename in QUERY_FILES:
            objective, df = run_query(conn, filename)
            results.append({"archivo": filename, "objetivo": objective, "resultado": df})
        return results
    finally:
        conn.close()
