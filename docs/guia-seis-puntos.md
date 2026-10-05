# Cómo repetir los seis puntos de la demo

Guía para otra persona del grupo. El laboratorio es local y didáctico. El servidor, si se enciende, escucha solo en esta computadora. La muestra generada por inteligencia artificial no la ejecuta la aplicación: Semgrep la lee como código fuente.

Repositorio del grupo: https://github.com/ChethhSito/Seguridad---Grupo3

Los comandos de abajo son para PowerShell, parados en la carpeta del proyecto. En Linux o macOS la herramienta está en `.venv/bin/semgrep` y Python en `.venv/bin/python`.

## Antes de empezar

1. Instala Python 3.10 o superior.
2. Clona el repositorio y entra a la carpeta.
3. Crea el entorno e instala las dependencias:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt semgrep
```

4. Comprueba que Semgrep responda:

```powershell
.\.venv\Scripts\semgrep.exe --version
```

Tiene que imprimir un número de versión. Si la ventana se cierra sola y no imprime nada, Windows está bloqueando el motor `semgrep-core.exe`. Primero, en las propiedades de ese archivo (está en `.venv\Lib\site-packages\semgrep\bin\`), marca **Desbloquear** si aparece. Si sigue sin arrancar, el Control de aplicaciones inteligentes no permite una excepción solo para ese programa. Léelo antes de apagarlo: si la pantalla dice que no podrás volver a encenderlo sin reinstalar Windows, no lo apagues. Sin esa versión en pantalla, los escaneos de esta guía no corren.

5. Opcional, para ver el laboratorio en el navegador:

```powershell
.\.venv\Scripts\python.exe app.py
```

Abre `http://127.0.0.1:5000/`. Hay dos búsquedas y dos saludos: una versión insegura y una corregida en cada caso. Ciérralo con Ctrl+C cuando termines. No hace falta tenerlo encendido para escanear.

## Punto 27. Instalar Semgrep y dejar las reglas listas

Qué se demuestra: la herramienta está instalada y usa las reglas del proyecto, no solo las que vienen de fábrica.

1. El paso de instalación de arriba cubre la primera mitad.
2. Abre `reglas.yml`. Ahí están las reglas del grupo.
3. Ejecuta:

```powershell
.\.venv\Scripts\semgrep.exe scan --config reglas.yml --metrics=off app.py
```

Qué debes ver: **2 hallazgos**, los dos en `app.py`. Uno en la búsqueda que arma la consulta SQL con el texto del usuario. Otro en el saludo que marca el HTML como confiable.

Comprobación automática:

```powershell
.\.venv\Scripts\python.exe scripts\verificar_hallazgos.py
```

Termina en OK solo si siguen siendo exactamente esos dos.

## Punto 30. Regla escrita por el grupo

Conviene mostrarlo justo después del escaneo anterior, con `reglas.yml` abierto.

Cada regla tiene:

- un identificador, para saber cuál saltó;
- el lenguaje;
- la severidad;
- el mensaje que explica el problema;
- el patrón que Semgrep busca;
- la categoría OWASP y el CWE, en los datos de la regla.

El patrón no es una frase suelta. Describe la forma del código. Por ejemplo, la regla de SQL reconoce una llamada `execute` cuya consulta está armada con una cadena interpolada. La versión corregida separa la consulta y el dato, así que esa regla no la marca.

Señala en voz alta el identificador, el patrón, el mensaje y la línea del hallazgo. Con eso el punto queda mostrado.

## Punto 28. Escanear código generado por inteligencia artificial

Qué se demuestra: Semgrep también revisa un archivo distinto de la aplicación, escrito como muestra de código generado por un modelo.

Ese archivo es `muestras/codigo_generado_ia.py`. El listado `muestras/dependencias-ia.txt` solo existe para que una regla tenga un texto que leer. No se instala.

```powershell
.\.venv\Scripts\semgrep.exe scan --config reglas.yml --metrics=off muestras/codigo_generado_ia.py muestras/dependencias-ia.txt
.\.venv\Scripts\python.exe scripts\verificar_muestra_ia.py
```

Qué debes ver: **11 hallazgos**. El segundo comando termina en OK si los identificadores no cambiaron.

La aplicación no importa esos archivos. Aunque `app.py` esté apagado, el escaneo igual funciona, porque Semgrep no necesita ejecutar el programa.

## Punto 29. Detección del OWASP Top 10 Web

Los 11 hallazgos del punto anterior son este punto. Hay diez categorías. La inyección aparece dos veces, una por SQL y otra por HTML.

| Regla | Categoría |
| --- | --- |
| `laboratorio-acceso-por-parametro` | A01 Control de acceso roto |
| `laboratorio-hash-md5` | A02 Fallas criptográficas |
| `laboratorio-sql-fstring` | A03 Inyección, SQL |
| `laboratorio-html-markup-fstring` | A03 Inyección, HTML |
| `laboratorio-assert-autorizacion` | A04 Diseño inseguro |
| `laboratorio-debug-flask` | A05 Configuración de seguridad incorrecta |
| `laboratorio-dependencia-antigua` | A06 Componentes vulnerables u obsoletos |
| `laboratorio-password-fijo` | A07 Fallas de identificación y autenticación |
| `laboratorio-pickle` | A08 Fallas de integridad del software y de los datos |
| `laboratorio-log-credencial` | A09 Fallas de registro y monitoreo |
| `laboratorio-urlopen-destino` | A10 Falsificación de petición del lado del servidor |

En la demo, lee el mensaje de cada hallazgo y di la categoría. No hace falta presentarlos como once fallas independientes de una aplicación en producción: son patrones preparados para que la regla los encuentre.

La versión corregida está en `muestras/referencias_seguras.py` y `muestras/dependencias-seguras.txt`. Si se escanean con las mismas reglas, no deben aparecer hallazgos. Eso se comprueba en el punto 32.

También puedes lanzar el escaneo comunitario sobre la aplicación:

```powershell
.\.venv\Scripts\semgrep.exe scan --config auto app.py
```

El número de avisos puede cambiar según la versión de Semgrep. Varios avisos suelen señalar el mismo fragmento. No los cuentes como vulnerabilidades distintas.

## Punto 32. GitHub Actions como pre-commit

Qué se demuestra: antes de guardar un cambio, y también en GitHub, se puede impedir que la corrección vuelva a tener los patrones inseguros.

El laboratorio vulnerable se queda en el repositorio para poder repetir la demo. La puerta no intenta borrar esos ejemplos. Vigila la corrección.

En esta computadora:

```powershell
.\.venv\Scripts\python.exe scripts\precommit_semgrep.py
```

Qué debes ver: un OK. El código corregido no dispara las reglas.

Para dejar el mismo control enganchado a Git:

```powershell
.\.venv\Scripts\python.exe -m pip install pre-commit
.\.venv\Scripts\pre-commit.exe install
```

A partir de ahí, cada commit de esta copia local ejecuta `.pre-commit-config.yaml`, que llama a ese mismo script.

Para enseñar que la puerta sí sabe detenerse, escanea la muestra de IA pidiendo error:

```powershell
.\.venv\Scripts\semgrep.exe scan --config reglas.yml --error --metrics=off muestras/codigo_generado_ia.py muestras/dependencias-ia.txt
```

Ese comando termina con un código distinto de cero, porque ahí sí hay hallazgos. No hace falta guardar ese resultado.

En GitHub, el archivo `.github/workflows/semgrep.yml` corre en cada push y en cada pull request. Hace cuatro cosas:

1. Pruebas del laboratorio.
2. Escaneo de `app.py` con reglas comunitarias.
3. Comprobación de que los dos hallazgos didácticos de `app.py` sigan ahí.
4. Bloqueo si la corrección vuelve a coincidir con una regla, y comprobación de que la muestra de IA conserve sus once hallazgos.

El resultado se mira en la pestaña Actions del repositorio. En el commit *Cambios Finales Entregable 1* las dos revisiones quedaron en verde.

También puedes correr las pruebas locales:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Punto 31. Triaje automático en la plataforma

Este punto no se resuelve solo con archivos del repositorio. Los hallazgos tienen que verse en la plataforma de Semgrep, donde la inteligencia artificial puede indicar si conviene corregirlos o si parecen un falso positivo. En 2026 esa función se llama Semgrep Multimodal. Antes se presentaba como Assistant.

La forma que ya funcionó con esta carpeta es subir el escaneo desde la consola, sin pedir que el dueño del repositorio instale una aplicación en GitHub.

1. Entra a https://semgrep.dev y crea la cuenta con GitHub, o entra si ya existe.
2. En **Settings**, **Global**, activa **Semgrep Multimodal** si el interruptor aparece. Si ofreces **Autofix**, déjalo sin marcar: así no se abren pull requests ni se pide permiso de escritura.
3. En la carpeta del proyecto:

```powershell
.\.venv\Scripts\semgrep.exe login
```

Se abre el navegador. Pulsa **Activate**.

4. Sube el escaneo:

```powershell
.\.venv\Scripts\semgrep.exe ci
```

5. En la plataforma abre **Code**. Debe aparecer el proyecto de esta carpeta, con hallazgos en `app.py` y en `muestras/codigo_generado_ia.py`.
6. Abre uno, por ejemplo la inyección SQL de Flask. La evidencia del punto es la ficha del hallazgo, no solo la lista. Guarda una captura.

Si más adelante quieres el escaneo continuo desde GitHub, en **Scan new project** elige **CLI** si la aplicación de GitHub está instalada solo en tu cuenta: esa aplicación ve tus repositorios, no automáticamente los de otra persona. El repositorio del grupo es `ChethhSito/Seguridad---Grupo3`. Tu copia personal, si existe, es otro proyecto.

No pegues el token de Semgrep en el chat, en una captura ni en el repositorio. Al autorizar GitHub, elige solo el repositorio que quieras escanear.

## Orden corto para ensayar

1. `semgrep.exe --version`
2. Escanear `app.py` con `reglas.yml` y abrir una regla.
3. Escanear la muestra de IA y recorrer las categorías.
4. Correr `scripts\precommit_semgrep.py` y mostrar el workflow de GitHub.
5. Entrar a la plataforma y abrir un hallazgo subido con `semgrep ci`.

## Si algo no cuadra

| Lo que pasa | Qué revisar |
| --- | --- |
| `semgrep.exe --version` no imprime nada | Windows está bloqueando `semgrep-core.exe`. |
| El escaneo de `app.py` no da 2 hallazgos | Tiene que usarse `--config reglas.yml` y el archivo `app.py` de este repositorio. |
| La muestra no da 11 hallazgos | Incluye los dos archivos: el de Python y `muestras/dependencias-ia.txt`. |
| `precommit_semgrep.py` dice que Semgrep no pudo ejecutarse | Es el mismo bloqueo de Windows, no un hallazgo nuevo. |
| En la plataforma el proyecto sale en cero y dice *Scanning* | El escaneo todavía no terminó. Espera y vuelve a abrir **Code**. |
| No aparece el repositorio del grupo al conectar GitHub | La aplicación está en tu usuario. Usa `semgrep ci` desde esta carpeta. |
