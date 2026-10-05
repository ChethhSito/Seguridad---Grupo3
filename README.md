# Grupo 3 · Parcial: Semgrep

Laboratorio **local y deliberadamente vulnerable** para explicar análisis estático de código (SAST). La aplicación Flask ofrece dos pares de rutas: una búsqueda con SQL injection y un saludo con XSS; cada ruta insegura tiene una versión corregida. Las reglas propias detectan los dos patrones inseguros. El proyecto es material didáctico, no una aplicación para producción.

## Requisitos

- Python 3.10 o superior
- Semgrep CLI
- Un entorno local autorizado. El servidor escucha solamente en `127.0.0.1`.

## Instalación en PowerShell

```powershell
cd H:\seguridad\grupo3-semgrep
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt semgrep
```

En Linux/macOS cambia las rutas del entorno virtual por `.venv/bin/python`.

Si `semgrep.exe --version` termina al instante y no imprime la versión, Windows está bloqueando el motor (`semgrep-core.exe`, código `0xC0E90002`). Hay que permitir ese archivo en Seguridad de Windows, en Control de aplicaciones inteligentes, antes de la demo en esta máquina.

## Ejecutar el laboratorio

```powershell
.\.venv\Scripts\python.exe app.py
```

Abre `http://127.0.0.1:5000/`. La página inicial tiene formularios para probar cada caso y un enlace al reporte de Semgrep. Las rutas son:

| Caso | Vulnerable | Corregida |
| --- | --- | --- |
| Consulta SQL | `/inseguro/buscar?nombre=ana` | `/seguro/buscar?nombre=ana` |
| Salida HTML | `/inseguro/saludo?nombre=ana` | `/seguro/saludo?nombre=ana` |

La base SQLite está en memoria y contiene solo `ana` y `luis`. Reiniciar el servidor restablece el laboratorio.

## Escanear

```powershell
.\.venv\Scripts\semgrep.exe scan --config reglas.yml app.py
.\.venv\Scripts\semgrep.exe scan --config auto app.py
```

El primer comando ejecuta dos reglas creadas para esta demo y debe mostrar **dos hallazgos**. El segundo usa reglas comunitarias elegidas automáticamente; sus resultados pueden variar según la versión y las reglas publicadas. Para exportar evidencia:

```powershell
.\.venv\Scripts\semgrep.exe scan --config reglas.yml --json app.py > hallazgos.json
```

`hallazgos.json` es evidencia generada; revisa su contenido antes de compartirlo. El archivo fuente contiene patrones inseguros intencionales.

## Muestra generada por IA

`muestras/codigo_generado_ia.py` y `muestras/dependencias-ia.txt` son código generado para el escaneo. No los importa `app.py` y el servidor no los ejecuta. `muestras/referencias_seguras.py` y `muestras/dependencias-seguras.txt` son la corrección.

```powershell
.\.venv\Scripts\semgrep.exe scan --config reglas.yml --metrics=off muestras/codigo_generado_ia.py muestras/dependencias-ia.txt
.\.venv\Scripts\python.exe scripts\verificar_muestra_ia.py
```

El primer comando debe mostrar **11 hallazgos**, uno por cada categoría del OWASP Top 10 Web (la inyección aparece dos veces: SQL y XSS). El segundo termina en OK solo si siguen siendo exactamente esos identificadores.

| Regla | OWASP 2021 |
| --- | --- |
| `laboratorio-acceso-por-parametro` | A01 Broken Access Control |
| `laboratorio-hash-md5` | A02 Cryptographic Failures |
| `laboratorio-sql-fstring` y `laboratorio-html-markup-fstring` | A03 Injection |
| `laboratorio-assert-autorizacion` | A04 Insecure Design |
| `laboratorio-debug-flask` | A05 Security Misconfiguration |
| `laboratorio-dependencia-antigua` | A06 Vulnerable and Outdated Components |
| `laboratorio-password-fijo` | A07 Identification and Authentication Failures |
| `laboratorio-pickle` | A08 Software and Data Integrity Failures |
| `laboratorio-log-credencial` | A09 Security Logging and Monitoring Failures |
| `laboratorio-urlopen-destino` | A10 Server-Side Request Forgery |

`dependencias-ia.txt` solo existe para que la regla A06 tenga un patrón que leer. No se instala.

## Bloqueo en pre-commit y en GitHub Actions

El código vulnerable del laboratorio permanece en el repositorio para poder repetir la demo. El bloqueo protege la corrección: si `referencias_seguras.py` o `dependencias-seguras.txt` vuelven a coincidir con una regla, el chequeo falla.

```powershell
.\.venv\Scripts\python.exe -m pip install pre-commit
.\.venv\Scripts\pre-commit.exe install
.\.venv\Scripts\python.exe scripts\precommit_semgrep.py
```

Para enseñar el fallo, el mismo escaneo con `--error` sobre la muestra de IA termina con código distinto de cero. En GitHub Actions, `.github/workflows/semgrep.yml` repite ese bloqueo en cada push y pull request, y `scripts/verificar_muestra_ia.py` impide que desaparezcan los hallazgos de la muestra.

Semgrep Assistant, el triaje automático en la plataforma, necesita una cuenta del equipo y no forma parte de este entorno local.

## Ver los hallazgos en HTML

Ya se incluye [un reporte HTML listo para abrir](reportes/semgrep.html). Haz doble clic en el archivo o ábrelo desde el navegador. Para actualizarlo después de editar el código:

```powershell
.\.venv\Scripts\python.exe scripts\generar_reporte.py
```

El generador ejecuta Semgrep dos veces: con `reglas.yml` y con `--config auto`. La segunda ejecución puede requerir conexión para obtener las reglas comunitarias. El HTML es autocontenido y se puede abrir después sin conexión.

Los avisos comunitarios se explican en español en el reporte. Cada tarjeta conserva el identificador de la regla y permite desplegar el mensaje original en inglés para contrastarlo con la salida de Semgrep.

## Qué demuestra cada regla

- `laboratorio-sql-fstring`: detecta una llamada `execute` con una consulta construida por `f-string`. La ruta segura usa un marcador `?` y pasa el valor como parámetro.
- `laboratorio-html-markup-fstring`: detecta `Markup` aplicado a HTML interpolado. La ruta segura usa `render_template` y `templates/saludo.html` para que Jinja escape el contenido.

Estas reglas buscan **patrones concretos**, no prueban la explotabilidad por sí solas ni cubren todas las variantes de SQL injection o XSS. Revisar cada hallazgo forma parte del análisis.

## Pruebas y CI

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

El workflow de GitHub Actions ejecuta las pruebas, el escaneo del laboratorio y la puerta sobre el código corregido. Los hallazgos de `app.py` y de la muestra de IA se conservan a propósito, para poder repetir la demo. La puerta sí falla si `muestras/referencias_seguras.py` o `muestras/dependencias-seguras.txt` vuelven a coincidir con una regla.

También ejecuta las pruebas funcionales y `scripts/verificar_hallazgos.py`, que falla si cambia el número o el identificador de los dos hallazgos de `app.py`. El script busca Semgrep dentro de `.venv` y, si no está, en el `PATH`. Puedes ejecutarlo con `.\.venv\Scripts\python.exe scripts\verificar_hallazgos.py`.

## Entregables sugeridos

- [Guía para repetir los seis puntos](docs/guia-seis-puntos.md)
- [Guion de demo](docs/demo.md)
- [Base del informe técnico](docs/informe.md)
- Captura o video de la ejecución, y `hallazgos.json` revisado
- Presentación con arquitectura, hallazgos y correcciones

El enunciado completo está en `../instrucciones.md`.
