-- Esquema de la base de datos de fundamentales.
-- empresas: un snapshot de métricas fundamentales por empresa.
-- precios_historicos: serie de precios de cierre, relacionada con empresas
-- por ticker -- existe para poder hacer un JOIN real entre ambas tablas.

CREATE TABLE IF NOT EXISTS empresas (
    ticker TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    sector TEXT NOT NULL,
    market_cap REAL,
    per REAL,
    margen_beneficio REAL,
    crecimiento_ingresos REAL
);

CREATE TABLE IF NOT EXISTS precios_historicos (
    ticker TEXT NOT NULL,
    fecha TEXT NOT NULL,
    precio_cierre REAL NOT NULL,
    PRIMARY KEY (ticker, fecha),
    FOREIGN KEY (ticker) REFERENCES empresas(ticker)
);
