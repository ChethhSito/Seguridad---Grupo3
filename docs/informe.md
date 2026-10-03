# Informe técnico base · Parcial Grupo 3

> Completar autores, fecha, capturas y resultados reales antes de exportar a PDF. Límite del curso: 15 páginas.

## Portada

**Título:** Detección de patrones de SQL injection y XSS con Semgrep  
**Curso:** Seguridad Informática / Ciberseguridad · 2026-II  
**Grupo:** 3  
**Integrantes y roles:** [completar]  
**Docente y fecha:** [completar]

## 1. Objetivo

Evaluar si Semgrep identifica dos patrones inseguros deliberados en una aplicación Flask local, crear reglas propias y comparar el código vulnerable con su alternativa corregida.

## 2. Alcance y entorno

El alcance es `app.py` y las reglas en `reglas.yml`. Se utiliza Python, Flask y SQLite en memoria. Todo ocurre en un laboratorio local autorizado; no se prueban servicios externos.

**Versiones verificadas localmente:** Python 3.12.6, Semgrep 1.179.0 y Flask 3.1.3.  
**Comandos de instalación y ejecución:** reproducir los de `README.md`.

## 3. Fundamento técnico

SAST inspecciona código fuente sin necesidad de ejecutar la aplicación. Semgrep compara el código con reglas que describen estructuras sintácticas y, según el motor y la regla, puede usar análisis más profundo. Un hallazgo requiere revisión humana para confirmar impacto y contexto. Las reglas de este proyecto usan coincidencia estructural sencilla.

**Arquitectura del laboratorio:** navegador o cliente HTTP → Flask (`app.py`) → SQLite en memoria para búsqueda; las rutas de saludo devuelven HTML. Semgrep lee `app.py` desde la CLI y reporta coincidencias de `reglas.yml`.

## 4. Implementación y hallazgos

| ID de regla | Patrón de la demo | Riesgo | Corrección |
| --- | --- | --- | --- |
| `laboratorio-sql-fstring` | `execute(f"...")` | Datos incorporados a una consulta SQL | Consulta parametrizada con `?` |
| `laboratorio-html-markup-fstring` | `Markup(f"...")` | HTML de entrada tratado como confiable | Plantilla con autoescape |

**Resultado local verificado:** las reglas propias produjeron 2 hallazgos, uno en `buscar_inseguro` y otro en `saludo_inseguro`. El escaneo comunitario con `--config auto` produjo 8 hallazgos, incluidos varios avisos sobre el mismo fragmento vulnerable. Las 3 pruebas funcionales pasaron; muestran que la entrada de prueba altera la consulta insegura y que el HTML sin escape aparece únicamente en la ruta insegura. Estos resultados corresponden a la versión y reglas disponibles al preparar este repositorio; deben repetirse antes de la exposición.

**Evidencia por completar:** capturas de la ejecución, líneas de cada hallazgo, revisión individual de los 8 avisos comunitarios y salida tras probar la corrección en una copia temporal. Varios avisos apuntan al mismo código; no deben contarse como 8 vulnerabilidades independientes.

## 5. Procedimiento reproducible

1. Crear entorno virtual e instalar `requirements.txt` y Semgrep.
2. Ejecutar `python -m unittest discover -s tests -v`.
3. Ejecutar `semgrep scan --config reglas.yml app.py` y registrar resultado.
4. Ejecutar `semgrep scan --config auto app.py` y registrar resultado por separado.
5. Comparar cada ruta insegura con su versión segura.
6. Revisar el workflow de `.github/workflows/semgrep.yml` y guardar evidencia de su ejecución en GitHub.

## 6. Limitaciones

Las dos reglas personalizadas detectan únicamente las formas escritas en `reglas.yml`: no demuestran cobertura universal de SQL injection ni XSS. La salida de `--config auto` puede variar con las reglas disponibles. La plataforma Semgrep Assistant y sus funciones de IA requieren configuración y acceso propios; no forman parte de esta demo local hasta que el equipo pueda verificarlos.

## 7. Conclusiones

Las reglas propias localizaron los dos patrones inseguros preparados para el laboratorio. Las pruebas funcionales confirmaron el efecto de la entrada de ejemplo y el comportamiento de las rutas corregidas. El escaneo comunitario generó varios avisos para dos zonas de código, por lo que la interpretación requiere deduplicar y revisar cada resultado. [Añadir aquí conclusiones del equipo tras repetir la demo.]

## 8. Referencias

- Semgrep. *Local and CLI scans*. https://semgrep.dev/docs/category/local-and-cli-scans
- Semgrep. *Writing Semgrep rules*. https://semgrep.dev/docs/writing-rules/overview/
- Semgrep. *Sample CI configurations*. https://semgrep.dev/docs/semgrep-ci/sample-ci-configs
- OWASP. *SQL Injection Prevention Cheat Sheet*. https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
- OWASP. *Cross Site Scripting Prevention Cheat Sheet*. https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
