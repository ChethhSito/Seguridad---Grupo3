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

El workflow de GitHub Actions ejecuta un escaneo comunitario y uno con reglas propias. El segundo conserva los hallazgos esperados como demostración; su presencia no bloquea el workflow. Para un proyecto real, corrijan las fallas y configuren el escaneo como puerta de seguridad.

También ejecuta las pruebas funcionales y `scripts/verificar_hallazgos.py`, que falla si cambia el número o el identificador de los hallazgos didácticos. Para ejecutar esta comprobación en Windows, activa primero `.venv` o agrega su carpeta `Scripts` al `PATH`.

## Entregables sugeridos

- [Guion de demo](docs/demo.md)
- [Base del informe técnico](docs/informe.md)
- Captura o video de la ejecución, y `hallazgos.json` revisado
- Presentación con arquitectura, hallazgos y correcciones

El enunciado completo está en `../instrucciones.md`.
