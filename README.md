# 🗄️ Proyecto 4 — Base de Datos de Fundamentales en SQL

> 18 empresas, 2 tablas relacionadas, 4 preguntas de negocio respondidas en SQL puro — la segunda habilidad técnica explícita de la oferta de referencia (Quant Analyst Sales).

![SQLite](https://img.shields.io/badge/SQLite-base%20de%20datos-003B57?logo=sqlite&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-consultas%20documentadas-4479A1?logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-dashboard-3F4F75?logo=plotly&logoColor=white)

---

## Qué hace

Carga datos fundamentales (sector, capitalización, PER, margen de beneficio, crecimiento de ingresos) de 18 empresas en una base de datos relacional **SQLite**, junto con su histórico de precios reciente, y responde 4 preguntas de negocio reales con consultas SQL — cada una documentada con su objetivo antes que su código. A diferencia de los Proyectos 1-3, el protagonista aquí no es el análisis en Python sino el modelo de datos y el SQL en sí.

## Vista previa del dashboard

La versión interactiva completa está en [`outputs/dashboard.html`](outputs/dashboard.html): ábrelo con doble clic, no necesita servidor. Muestra 2 gráficos de apoyo y una tarjeta por consulta con su tabla de resultado.

## Estructura del proyecto

Primera estructura del portfolio con una carpeta `db/` (esquema + base de datos) y una carpeta `sql/` con archivos `.sql` reales versionados — lo que hace visible en el repo que el proyecto es, ante todo, un ejercicio de SQL:

```
proyecto-4-fundamentales-sql/
├── README.md
├── requirements.txt
├── data/                 <- caché de fundamentales y precios descargados
├── db/
│   ├── schema.sql          <- DDL: definición de las tablas
│   └── fundamentales.db     <- base de datos SQLite generada (no versionada)
├── sql/                   <- una consulta por pregunta de negocio, documentada
│   ├── 01_ranking_per_por_sector.sql
│   ├── 02_mejor_margen_por_sector.sql
│   ├── 03_evolucion_metrica_por_sector.sql
│   └── 04_rentabilidad_reciente_por_empresa.sql
├── src/
│   ├── data.py              <- descarga fundamentales y precios (yfinance)
│   ├── build_db.py           <- crea el esquema y carga los datos en SQLite
│   ├── queries.py             <- ejecuta cada .sql vía pandas, expone el objetivo de negocio
│   ├── dashboard.py            <- dashboard interactivo (Plotly) -> outputs/dashboard.html
│   └── main.py                   <- orquesta el pipeline
└── outputs/               <- dashboard generado
```

## Esquema de la base de datos

```sql
CREATE TABLE empresas (
    ticker TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    sector TEXT NOT NULL,
    market_cap REAL,
    per REAL,
    margen_beneficio REAL,
    crecimiento_ingresos REAL
);

CREATE TABLE precios_historicos (
    ticker TEXT NOT NULL,
    fecha TEXT NOT NULL,
    precio_cierre REAL NOT NULL,
    PRIMARY KEY (ticker, fecha),
    FOREIGN KEY (ticker) REFERENCES empresas(ticker)
);
```

`precios_historicos` existe específicamente para poder hacer un **JOIN real** entre ambas tablas (consulta 04) — no solo `GROUP BY` sobre una tabla plana, que sería el error típico de un ejercicio de SQL demasiado simple.

## Cómo ejecutarlo

```bash
python -m venv venv
source venv/bin/activate  # en Windows: venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

Al terminar, la consola imprime cada consulta con su objetivo de negocio y su resultado, y se genera `outputs/dashboard.html`. La base de datos se recrea desde cero en cada ejecución (`db/fundamentales.db`), a partir de la caché en `data/`.

### Nota sobre certificados SSL
Mismo mecanismo que en los Proyectos 1-3: si `yfinance` falla con `CERTIFICATE_VERIFY_FAILED` (típico con antivirus que inspeccionan el tráfico HTTPS, p. ej. Norton), `src/data.py` usa automáticamente un bundle de certificados local en `.certs/cacert.pem` si existe.

## Las 4 consultas

| Archivo | Pregunta de negocio | Concepto SQL |
|---|---|---|
| `01_ranking_per_por_sector.sql` | ¿Qué empresas cotizan más baratas (PER bajo) dentro de cada sector? | `WHERE` (filtra filas) + `ORDER BY` |
| `02_mejor_margen_por_sector.sql` | ¿Qué empresa es la más rentable dentro de cada sector? | Subconsulta correlacionada (`MAX` por sector) |
| `03_evolucion_metrica_por_sector.sql` | Capitalización total y PER medio por sector | `GROUP BY` + `AVG`/`SUM` — contraste directo con `WHERE` |
| `04_rentabilidad_reciente_por_empresa.sql` | Rentabilidad reciente de cada empresa, cruzada con su PER | `JOIN` real entre `empresas` y `precios_historicos` |

## Resultados
_(snapshot al momento de ejecución; 18 empresas en 9 sectores)_

- **Tecnología** es, con diferencia, el sector con más peso (≈9.030 Bn de capitalización conjunta) y el más caro como bloque (PER medio 37.4, frente a 8.7 de Energía) — Apple, Microsoft, SAP y ASML.
- **Repsol** (PER 8.7, el más bajo de toda la cesta) fue también la empresa con mejor rentabilidad reciente (+45.3%): un caso donde "barata sobre el papel" y "el mercado la está premiando" coincidieron — no siempre es así, y es justo lo que la consulta 04 permite contrastar en una sola tabla.
- **LVMH** fue el caso contrario: PER intermedio (20.7) pero la peor rentabilidad reciente (-16.4%), reflejo del mismo enfriamiento del sector lujo europeo ya observado en el Proyecto 1.
- Por margen de beneficio, **Microsoft** lidera con holgura (40.3%) seguida de **Banco Santander** (33.5%) — confirma que comparar márgenes sector a sector (consulta 02) evita conclusiones erróneas: un margen del 33% es excepcional en banca, pero sería mediocre en software.

## Conceptos para poder explicar en entrevista

- **`WHERE` vs. `GROUP BY`**: `WHERE` filtra filas individuales *antes* de cualquier agregación; `GROUP BY` agrupa filas en bloques para aplicar una función de agregación (`AVG`, `SUM`, `COUNT`) a cada bloque — son operaciones en momentos distintos de la ejecución de la consulta, y `HAVING` (no usado aquí, pero hay que saber cuándo) filtraría *después* de agrupar.
- **JOIN**: por qué cruzar `empresas` y `precios_historicos` por `ticker` permite responder preguntas que ninguna de las dos tablas responde por separado — y por qué esto es justo lo que un CSV suelto no resuelve sin duplicar datos (repetir sector/PER en cada fila de precio, por ejemplo).
- **Por qué una base de datos relacional en vez de CSVs sueltos**: integridad referencial (`FOREIGN KEY`), evitar duplicación de datos, y la capacidad de responder preguntas nuevas con una consulta en vez de reescribir un script de pandas cada vez.
