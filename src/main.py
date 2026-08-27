"""Punto de entrada: descarga datos, construye la base de datos SQLite,
ejecuta las consultas documentadas y genera el dashboard."""

from build_db import build_database
from dashboard import build_dashboard
from data import load_or_download_fundamentals, load_or_download_recent_prices
from queries import run_all_queries


def main() -> None:
    empresas = load_or_download_fundamentals()
    precios = load_or_download_recent_prices()

    db_path = build_database(empresas, precios)
    print(f"Base de datos creada en {db_path} ({len(empresas)} empresas, {len(precios)} filas de precio)")

    results = run_all_queries(db_path)

    for r in results:
        print(f'\n=== {r["archivo"]} ===')
        print(r["objetivo"])
        print(r["resultado"].to_string(index=False))

    dashboard_path = build_dashboard(results, len(empresas))
    print(f"\nDashboard interactivo generado en: {dashboard_path}")


if __name__ == "__main__":
    main()
