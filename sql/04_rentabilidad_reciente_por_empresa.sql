-- Objetivo de negocio: ¿cómo se ha comportado el precio de cada empresa en
-- el periodo cargado? Cruza los fundamentales (tabla empresas) con el precio
-- real (tabla precios_historicos) para poder contrastar "barata sobre el
-- papel" (PER bajo) con "cómo la está tratando el mercado" (rentabilidad
-- reciente) en la misma consulta.
-- Concepto: JOIN real entre dos tablas relacionadas por ticker -- exactamente
-- lo que un CSV suelto no puede resolver sin duplicar datos.

WITH primer_precio AS (
    SELECT ticker, precio_cierre AS precio_inicial
    FROM precios_historicos
    WHERE (ticker, fecha) IN (
        SELECT ticker, MIN(fecha) FROM precios_historicos GROUP BY ticker
    )
),
ultimo_precio AS (
    SELECT ticker, precio_cierre AS precio_final
    FROM precios_historicos
    WHERE (ticker, fecha) IN (
        SELECT ticker, MAX(fecha) FROM precios_historicos GROUP BY ticker
    )
)
SELECT
    e.sector,
    e.nombre,
    e.ticker,
    e.per,
    ROUND((u.precio_final / p.precio_inicial - 1) * 100, 1) AS rentabilidad_pct
FROM empresas e
JOIN primer_precio p ON p.ticker = e.ticker
JOIN ultimo_precio u ON u.ticker = e.ticker
ORDER BY rentabilidad_pct DESC;
