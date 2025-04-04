@echo off
cd /d C:\Users\mattia.forneron\Desktop\myfolder\MyWorkFolder\eurofork\prj_02\codice_py

echo Avvio ambiente virtuale con cmd...
call .\.venv\Scripts\activate.bat

echo Start del server...
.\dist\start_server.exe

pause
