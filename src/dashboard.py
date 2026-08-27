"""Dashboard HTML interactivo con Plotly: un único archivo autocontenido en outputs/.

Mismo sistema de diseño que Proyectos 1-3 (paleta ya validada con el script de
accesibilidad del skill dataviz). A diferencia de esos proyectos, aquí el
protagonista es el resultado de cada consulta SQL -- el dashboard es
principalmente tablas, con un par de gráficos de apoyo.
"""

from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

OUTPUTS_DIR = Path(__file__).resolve().parent.parent / "outputs"

BLUE = "#2a78d6"
CATEGORICAL = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]

SURFACE = "#fcfcfb"
PAGE_PLANE = "#f9f9f7"
INK_PRIMARY = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
GRIDLINE = "#e1e0d9"
BASELINE = "#c3c2b7"
GOOD = "#006300"
CRITICAL = "#d03b3b"
BORDER = "rgba(11,11,11,0.10)"

FONT_FAMILY = 'system-ui, -apple-system, "Segoe UI", sans-serif'

TITLES = {
    "01_ranking_per_por_sector.sql": "Ranking de PER por sector",
    "02_mejor_margen_por_sector.sql": "Mejor margen de beneficio por sector",
    "03_evolucion_metrica_por_sector.sql": "Capitalización y PER medio por sector",
    "04_rentabilidad_reciente_por_empresa.sql": "Rentabilidad reciente por empresa",
}


def _base_layout(title: str, **extra) -> dict:
    layout = dict(
        title=dict(text=title, font=dict(family=FONT_FAMILY, size=15, color=INK_PRIMARY)),
        font=dict(family=FONT_FAMILY, size=12, color=INK_SECONDARY),
        paper_bgcolor=SURFACE,
        plot_bgcolor=SURFACE,
        legend=dict(font=dict(color=INK_SECONDARY, size=11), bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=50, r=30, t=50, b=40),
    )
    layout.update(extra)
    return layout


def _axis(**extra) -> dict:
    axis = dict(
        gridcolor=GRIDLINE,
        gridwidth=1,
        linecolor=BASELINE,
        tickfont=dict(color=INK_MUTED, size=11),
        title_font=dict(color=INK_SECONDARY, size=12),
        zeroline=False,
    )
    axis.update(extra)
    return axis


def _per_medio_figure(sector_df: pd.DataFrame) -> go.Figure:
    df = sector_df.sort_values("per_medio")
    colors = [CATEGORICAL[i % len(CATEGORICAL)] for i in range(len(df))]
    fig = go.Figure(
        go.Bar(
            x=df["per_medio"], y=df["sector"], orientation="h",
            marker=dict(color=colors),
            hovertemplate="%{y}: PER medio %{x}<extra></extra>",
        )
    )
    fig.update_layout(
        **_base_layout(
            "PER medio por sector",
            xaxis=_axis(title="PER medio"),
            yaxis=_axis(),
            showlegend=False,
        )
    )
    return fig


def _rentabilidad_figure(rentabilidad_df: pd.DataFrame) -> go.Figure:
    df = rentabilidad_df.sort_values("rentabilidad_pct")
    colors = [GOOD if v >= 0 else CRITICAL for v in df["rentabilidad_pct"]]
    fig = go.Figure(
        go.Bar(
            x=df["rentabilidad_pct"], y=df["nombre"], orientation="h",
            marker=dict(color=colors),
            hovertemplate="%{y}: %{x:+.1f}%<extra></extra>",
        )
    )
    fig.add_vline(x=0, line_color=BASELINE, line_width=1)
    fig.update_layout(
        **_base_layout(
            "Rentabilidad reciente por empresa",
            xaxis=_axis(title="Rentabilidad (%)"),
            yaxis=_axis(),
            showlegend=False,
            height=520,
        )
    )
    return fig


def _dataframe_to_html(df: pd.DataFrame) -> str:
    formatted = df.copy()
    for col in formatted.columns:
        if formatted[col].dtype.kind in "f":
            formatted[col] = formatted[col].map(lambda v: f"{v:,.1f}" if pd.notna(v) else "—")
    return formatted.to_html(classes="summary-table", index=False, border=0)


def build_dashboard(query_results: list[dict], n_empresas: int) -> Path:
    by_file = {r["archivo"]: r for r in query_results}

    per_chart_html = pio.to_html(
        _per_medio_figure(by_file["03_evolucion_metrica_por_sector.sql"]["resultado"]),
        full_html=False, include_plotlyjs="cdn", config={"displaylogo": False},
    )
    rentab_chart_html = pio.to_html(
        _rentabilidad_figure(by_file["04_rentabilidad_reciente_por_empresa.sql"]["resultado"]),
        full_html=False, include_plotlyjs=False, config={"displaylogo": False},
    )

    query_cards = ""
    for r in query_results:
        title = TITLES.get(r["archivo"], r["archivo"])
        query_cards += f"""<div class="card">
  <h2>{title}</h2>
  <p class="objective">{r["objetivo"]}</p>
  {_dataframe_to_html(r["resultado"])}
</div>
"""

    n_sectores = len(by_file["03_evolucion_metrica_por_sector.sql"]["resultado"])

    page = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Proyecto 4 — Fundamentales en SQL</title>
<style>
  :root {{
    --surface: {SURFACE};
    --page-plane: {PAGE_PLANE};
    --ink-primary: {INK_PRIMARY};
    --ink-secondary: {INK_SECONDARY};
    --ink-muted: {INK_MUTED};
    --gridline: {GRIDLINE};
    --border: {BORDER};
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: {FONT_FAMILY};
    margin: 0;
    background: var(--page-plane);
    color: var(--ink-primary);
  }}
  .wrap {{ max-width: 1080px; margin: 0 auto; padding: 0 24px 64px; }}

  .hero {{
    background: linear-gradient(135deg, #1a2e4a 0%, #2a78d6 100%);
    color: #ffffff;
    padding: 48px 24px 40px;
    margin-bottom: 28px;
  }}
  .hero-inner {{ max-width: 1080px; margin: 0 auto; }}
  .hero h1 {{ font-size: 1.75rem; margin: 0 0 8px; font-weight: 700; }}
  .hero p {{ margin: 0; color: rgba(255,255,255,0.85); font-size: 0.95rem; }}
  .hero .meta {{ margin-top: 18px; font-size: 0.8rem; color: rgba(255,255,255,0.65); letter-spacing: 0.02em; }}

  .card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 22px;
  }}
  .card h2 {{ font-size: 1.05rem; margin: 0 0 8px; color: var(--ink-primary); font-weight: 600; }}
  .objective {{ font-size: 0.85rem; color: var(--ink-secondary); margin: 0 0 16px; line-height: 1.5; }}

  .summary-table {{ border-collapse: collapse; width: 100%; font-size: 0.85rem; }}
  .summary-table th {{
    text-align: right; padding: 8px 12px; color: var(--ink-muted);
    font-weight: 500; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.03em;
    border-bottom: 1px solid var(--gridline);
  }}
  .summary-table td {{
    padding: 8px 12px; text-align: right; border-bottom: 1px solid var(--gridline);
    color: var(--ink-primary); font-variant-numeric: tabular-nums;
  }}
  .summary-table th:nth-child(1), .summary-table td:nth-child(1),
  .summary-table th:nth-child(2), .summary-table td:nth-child(2) {{ text-align: left; }}
  .summary-table tbody tr:hover {{ background: var(--page-plane); }}

  footer {{ text-align: center; font-size: 0.78rem; color: var(--ink-muted); padding-top: 8px; }}
</style>
</head>
<body>

<div class="hero">
  <div class="hero-inner">
    <h1>Base de Datos de Fundamentales en SQL</h1>
    <p>{n_empresas} empresas en {n_sectores} sectores, cargadas en SQLite y consultadas con SQL puro.</p>
    <div class="meta">datos fundamentales y de precio vía yfinance</div>
  </div>
</div>

<div class="wrap">

<div class="card">
  <h2>PER medio por sector</h2>
  {per_chart_html}
</div>

<div class="card">
  <h2>Rentabilidad reciente por empresa</h2>
  {rentab_chart_html}
</div>

{query_cards}

<footer>Proyecto 4 · Roadmap Quant · SQLite + Python (pandas, yfinance, Plotly)</footer>

</div>
</body>
</html>"""

    OUTPUTS_DIR.mkdir(exist_ok=True)
    out_path = OUTPUTS_DIR / "dashboard.html"
    out_path.write_text(page, encoding="utf-8")
    return out_path
