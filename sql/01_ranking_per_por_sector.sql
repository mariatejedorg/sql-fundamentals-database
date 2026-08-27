-- Objetivo de negocio: dentro de cada sector, ¿qué empresas cotizan más
-- baratas relativas a beneficio (PER más bajo) y cuáles más caras? Útil como
-- primer filtro de "valor" dentro de un sector antes de un análisis más fino.
-- Concepto: WHERE filtra filas individuales (aquí, descarta PER nulos o
-- negativos, que no son comparables); ORDER BY hace el ranking, no GROUP BY.

SELECT
    sector,
    nombre,
    ticker,
    per
FROM empresas
WHERE per IS NOT NULL AND per > 0
ORDER BY sector, per ASC;
