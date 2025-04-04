@echo off
rem Si sposta nella directory dove è presente il file .jar
echo Mi sposto nella directory del file...
pause
cd /d "C:\Users\mattia.forneron\Desktop\Metabase"
cls
echo Adesso siamo in C:\Users\mattia.forneron\Desktop\Metabase:
dir
pause
cls

rem Controlla se il file metabase.jar è presente
echo Controllo se metabase.jar esiste...
if not exist metabase.jar (
    echo Errore: metabase.jar non trovato!
    pause
    exit /b
)else (
    echo File Trovato
)
timeout /t 20 
cls

echo Avvio Metabase...
echo Chiudi questa finestra solo se vuoi fermarlo!!
timeout /t 20 
cls

echo Avvio Metabase...
echo Attendere...
start /b java -jar metabase.jar

timeout /t 45 /nobreak >nul
cls
echo Apro browser all'indirizzo http://localhost:3000/dashboard/33
rem Apre il browser di Chrome sull'indirizzo passato
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" http://localhost:3000/dashboard/33