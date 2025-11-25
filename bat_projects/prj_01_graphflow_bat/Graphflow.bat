@echo off
echo Mi sposto nella cartella dove trovo il codice sorgente
cd /d C:\Users\mattia.forneron\Documents\GitHub\MyWorkFolder\py_projects\prj_01_graphflow_py\graphflow

echo Avvio ambiente virtuale con cmd...
call .venv\Scripts\activate.bat

echo Controllo presenza start_server.exe...
if exist .\dist\start_server.exe (
    echo Trovato start_server.exe, avvio...
    .\dist\start_server.exe
) else (
    echo ERRORE: start_server.exe non trovato!
)

pause

