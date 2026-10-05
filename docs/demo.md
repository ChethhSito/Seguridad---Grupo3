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
| 1–2 min | Abrir `buscar_inseguro` y `saludo_inseguro` junto a sus correcciones | Un caso separa el dato del SQL; el otro deja que Jinja escape el HTML. |
| 2–4 min | Ejecutar `semgrep scan --config reglas.yml app.py` | Leer archivo, línea, regla y mensaje de los dos hallazgos del laboratorio. |
| 4–5 min | Abrir `reglas.yml` | Identificar `id`, `pattern`, `message`, lenguaje, severidad y la categoría OWASP. |
| 5–7 min | Escanear `muestras/codigo_generado_ia.py` y `muestras/dependencias-ia.txt` | Es código generado por IA, no lo sirve la aplicación. Recorrer los 11 mensajes y su categoría OWASP. |
| 7–8 min | Abrir `muestras/referencias_seguras.py` y ejecutar `scripts/precommit_semgrep.py` | La corrección queda limpia. El mismo escaneo con `--error` sobre la muestra de IA sí detiene el proceso. |
| 8–9 min | Mostrar `.pre-commit-config.yaml` y `.github/workflows/semgrep.yml` | El hook y Actions repiten el bloqueo en cada cambio. |
| 9–10 min | Ejecutar `semgrep scan --config auto app.py` | Comparar reglas comunitarias y propias sin prometer un número fijo de hallazgos. |

Para mostrar una corrección en directo, copia `app.py` a un archivo temporal local, sustituye en esa copia el fragmento inseguro por el equivalente seguro y vuelve a escanear la copia. Mantén `app.py` intacto para que la demostración sea repetible.

## Preguntas que deben poder responder

- ¿Por qué SAST puede revisar el código sin arrancar la aplicación?
- ¿Qué diferencia hay entre un hallazgo y una vulnerabilidad confirmada?
- ¿Por qué `execute(query, (name,))` es más seguro que interpolar `name` en SQL?
- ¿Qué hace el autoescape de Jinja y por qué `Markup` puede anularlo?
- ¿Qué casos no detectan estas dos reglas específicas?
- ¿Qué aporta el análisis en cada cambio mediante CI?
- ¿Qué categoría del OWASP Top 10 corresponde a cada hallazgo de la muestra de IA?
- ¿Por qué el pre-commit deja pasar el laboratorio vulnerable y bloquea la corrección si esa corrección se rompe?
- ¿Cómo se muestra el triaje automático en la plataforma de Semgrep?

**Regla de uso:** no ejecutar las rutas inseguras fuera de `localhost` ni usar estas técnicas contra sistemas sin autorización.

