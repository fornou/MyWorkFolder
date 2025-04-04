import webbrowser
import subprocess
import time

# Avvia il server FastAPI
subprocess.Popen(["uvicorn", "app:app", "--reload"])

time.sleep(3)

# Apre il browser sulla pagina localhost
browser_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
webbrowser.get(browser_path).open("http://127.0.0.1:8000")

