import webbrowser
import subprocess
import time
import socket

# Trova IP locale
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

# Avvia il server FastAPI
subprocess.Popen(["uvicorn", "app:app", "--reload", "--host", "0.0.0.0", "--port", "8080"])

# Attende che il server sia pronto
time.sleep(3)

# Apre il browser sulla pagina
browser_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
webbrowser.get(browser_path).open(f"http://{local_ip}:8080")
