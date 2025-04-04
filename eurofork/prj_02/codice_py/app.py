from fastapi import FastAPI, Form, File, UploadFile
from formattatore_csv import formattatore_csv
from fastapi.responses import FileResponse, HTMLResponse  # Aggiungi HTMLResponse qui
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

#Cartella dove salvo i file caricati e formattati
UPLOAD_FOLDER = "uploads"

app = FastAPI()

# Dice all'app dove trovare i contenuti (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS regola chi puo' accedere e a che cosa
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Richieste da tutti i domini
    allow_credentials=True,
    allow_methods=["*"],  # Richieste di tutti i metodi HTTP
    allow_headers=["*"],  # Permetti tutti gli header presenti nelle richieste
)

#Pagina di home che mi permette il caricamento dei file
@app.get("/", response_class=HTMLResponse)
async def serve_home():
    with open("static/index.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())

@app.post("/upload/")
async def upload_file(
        file: UploadFile = File(...),
        commessa: str = Form(...)
    ):
    # Cartella Uploads dove salvo i file .csv formattati
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    #Percorso dove salvare il file
    temp_file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # Salva temporaneamente il file caricato in percorso
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Crea il formattatore_csv passando il percorso del file temporaneo, i campi data e il numero di commessa
    formatter = formattatore_csv(temp_file_path, ['Data\\Ora TX', 'Data\\Ora RX', 'Data\\Ora inizio'], commessa)

    #Converte le date in datetime accettate dal db
    formatter.converti_date()
    #Aggiunge campo id_commessa
    formatter.aggiungi_campo()
    #Fa scaricare il file formattato
    formatter.esporta_file()

    # Ottieni il percorso del file formattato
    formatted_file_path = formatter.get_url_destinazione()

    # Rimuovi il file temporaneo
    os.remove(temp_file_path)

    # Restituisci il file formattato permettendo lo scaricamento
    return FileResponse(formatted_file_path, media_type='application/octet-stream', filename=os.path.basename(formatted_file_path))
