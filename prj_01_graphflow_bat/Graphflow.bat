@echo off
echo Mi sposto nella cartella dove trovo il codice sorgente
cd /d C:\Users\mattia.forneron\Documents\GitHub\Projects_For_Eurofork\prj_01_graphflow_py\graphflow

echo Avvio ambiente virtuale con cmd...
call .venv\Scripts\activate.bat

echo Controllo presenza start_server.py...
if exist ".\start_server.py" (
    echo Trovato start_server.py, avvio...
    python start_server.py
) else (
    echo ERRORE: start_server.py non trovato!
)

pause
