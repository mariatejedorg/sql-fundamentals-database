-- Objetivo de negocio: ¿qué empresa es la más rentable (mejor margen de
-- beneficio) dentro de cada sector? Es la pregunta típica al construir una
-- cesta "calidad" sector a sector, en vez de comparar márgenes entre
-- sectores muy distintos entre sí (un margen del 8% puede ser excelente en
-- retail y mediocre en tecnología).
-- Concepto: subconsulta correlacionada -- para cada empresa, comprueba que su
-- margen es el máximo dentro de su propio sector.

SELECT
    e.sector,
    e.nombre,
    e.ticker,
    e.margen_beneficio
FROM empresas e
WHERE e.margen_beneficio = (
    SELECT MAX(e2.margen_beneficio)
    FROM empresas e2
    WHERE e2.sector = e.sector
)
ORDER BY e.margen_beneficio DESC;
