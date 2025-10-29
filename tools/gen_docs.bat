@echo off
REM Genere archivos HTML estáticos desde los .md en manual/
REM Uso: abrir cmd en la raíz del proyecto y ejecutar: tools\gen_docs.bat

if exist venv\Scripts\activate.bat (
    echo Activando entorno virtual (cmd)...
    call venv\Scripts\activate.bat
) else (
    echo No se encontró venv\Scripts\activate.bat. Asegurate de crear/activar el entorno virtual primero.
)

echo Generando HTML estático desde manual/*.md ...
python tools\md_to_html.py

if %ERRORLEVEL% NEQ 0 (
    echo Hubo un error al generar los HTML. Verifica que 'markdown' esté instalado en el venv.
    echo Para instalarlo: pip install markdown
    exit /b %ERRORLEVEL%
)

echo HTML generados en manual\html
exit /b 0
