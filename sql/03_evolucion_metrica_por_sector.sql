-- Objetivo de negocio: vista agregada por sector -- capitalización total,
-- PER medio y nº de empresas -- para saber qué sectores pesan más en la
-- cesta y si cotizan caros o baratos como bloque, no empresa a empresa.
-- Concepto: GROUP BY agrega FILAS en grupos (aquí, por sector); WHERE (en la
-- consulta 01) filtra filas individuales antes de agregar -- son operaciones
-- distintas y en distinto momento de la ejecución (WHERE antes de agrupar,
-- HAVING después si hiciera falta filtrar sobre el resultado agregado).

SELECT
    sector,
    COUNT(*) AS num_empresas,
    ROUND(SUM(market_cap) / 1e9, 1) AS cap_total_bn,
    ROUND(AVG(per), 1) AS per_medio,
    ROUND(AVG(margen_beneficio) * 100, 1) AS margen_medio_pct
FROM empresas
GROUP BY sector
ORDER BY cap_total_bn DESC;
