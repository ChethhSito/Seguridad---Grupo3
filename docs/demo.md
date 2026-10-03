# Guion de demostración · 10 minutos

## Preparación

1. Instala las dependencias y ejecuta las pruebas de `README.md`.
2. Comprueba que el servidor abra en `http://127.0.0.1:5000/`.
3. Deja abiertas `app.py`, `reglas.yml` y una terminal en la carpeta del proyecto.
4. Graba un video de respaldo antes de la exposición.

## Secuencia sugerida

| Tiempo | Acción | Qué explicar |
| --- | --- | --- |
| 0–1 min | Enseñar las cuatro rutas | Mismo comportamiento funcional con dos implementaciones. |
| 1–3 min | Abrir `buscar_inseguro` y `buscar_seguro` | La interpolación forma parte de la consulta; el parámetro separa dato y SQL. |
| 3–5 min | Abrir `saludo_inseguro` y `saludo_seguro` | `Markup` declara confiable el HTML; Jinja escapa una variable normal. |
| 5–7 min | Ejecutar `semgrep scan --config reglas.yml app.py` | Leer archivo, línea, regla y mensaje de cada hallazgo. |
| 7–8 min | Abrir `reglas.yml` | Identificar `id`, `pattern`, `message`, lenguaje y severidad. |
| 8–9 min | Ejecutar `semgrep scan --config auto app.py` | Comparar reglas comunitarias y propias sin prometer un número fijo de hallazgos. |
| 9–10 min | Mostrar pruebas y workflow | Explicar cómo repetir el análisis y qué límites tiene. |

Para mostrar una corrección en directo, copia `app.py` a un archivo temporal local, sustituye en esa copia el fragmento inseguro por el equivalente seguro y vuelve a escanear la copia. Mantén `app.py` intacto para que la demostración sea repetible.

## Preguntas que deben poder responder

- ¿Por qué SAST puede revisar el código sin arrancar la aplicación?
- ¿Qué diferencia hay entre un hallazgo y una vulnerabilidad confirmada?
- ¿Por qué `execute(query, (name,))` es más seguro que interpolar `name` en SQL?
- ¿Qué hace el autoescape de Jinja y por qué `Markup` puede anularlo?
- ¿Qué casos no detectan estas dos reglas específicas?
- ¿Qué aporta el análisis en cada cambio mediante CI?

**Regla de uso:** no ejecutar las rutas inseguras fuera de `localhost` ni usar estas técnicas contra sistemas sin autorización.

