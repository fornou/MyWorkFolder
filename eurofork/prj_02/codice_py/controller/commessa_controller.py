from fastapi import Form, File, Depends, HTTPException, UploadFile, APIRouter, Query
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from sqlalchemy.orm import Session
from database.database import get_db
from services.auth_service import get_current_user
from services.commessa_service import CommessaService
from util.formattatore_csv import FormattatoreCsv as formattatore_csv
import shutil, os
import jwt
import time
from dotenv import load_dotenv
import os

load_dotenv()

METABASE_SITE_URL = os.getenv("METABASE_SITE_URL")
METABASE_SECRET_KEY = os.getenv("METABASE_SECRET_KEY")
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER") 


def genera_metabase_iframe(element_id: int, commessa: str):
    try:
        print(f"element_id: {element_id}, commessa: {commessa}")
        payload = {
            "resource": {"dashboard": element_id},
            "params": {
                "commessa": [commessa]
            },
            "exp": round(time.time()) + (60 * 60 * 24) # 1 giorno
        }
        token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")

        return METABASE_SITE_URL + "/embed/dashboard/" + token +"#bordered=true&titled=true"
         
    except Exception as e:
        print(f"Errore: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Errore: {str(e)}")

class CommessaController:
    def __init__(self):
        self.router = APIRouter(prefix="/api/commessa", tags=["Commesse"])#, dependencies=[Depends(get_current_user)])
        self._add_routes()
 
    def _add_routes(self):
        self.router.get("/all")(self.get_all_commesse)
        self.router.get("/{commessa}/grafico")(self.get_grafico_commessa)
        self.router.get("/{commessa}")(self.get_commessa_by_nome)
        self.router.get("/search/{title}")(self.get_commessa_by_filter)
        self.router.post("/create")(self.create_commessa)
        self.router.post("/{commessa}/{categoria}/upload")(self.upload_file)

    def get_grafico_commessa(
        self,
        commessa: int,
        categoria: str = Query("micromissioni"),
        db: Session = Depends(get_db)
    ):
        try:
            commessa_service = CommessaService(db)
            commessa_data = commessa_service.get_commessa_by_id(commessa)

            # Dashboard diverse per categoria
            dashboard_ids = {
                "micromissioni": 66,
                "allarmi": 67  # sostituisci con l'ID reale per "Allarmi"
            }

            if categoria not in dashboard_ids:
                raise HTTPException(status_code=400, detail="Categoria non valida")

            dashboard_id = dashboard_ids[categoria]
            iframe_url = genera_metabase_iframe(dashboard_id, commessa_data.Nome)

            iframe_html = f'''
                <iframe
                    src="{iframe_url}"
                    frameborder="0"  
                    width="100%"
                    height="600"
                    allowtransparency
                ></iframe>
            '''
            return HTMLResponse(content=iframe_html)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Errore nel generare l'iframe: {str(e)}")

    def get_commessa_by_nome(self, commessa: int, db: Session = Depends(get_db)):
        try:
            commessa_service = CommessaService(db)
            commessa = commessa_service.get_commessa_by_id(commessa) 
            return {"ID_Commessa": commessa.ID_Commessa, "Nome": commessa.Nome}
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Errore nel recuperare la commessa per ID: {str(e)}")

    def get_all_commesse(self, db: Session = Depends(get_db)):
        try:
            commessa_service = CommessaService(db)
            commesse = commessa_service.list_commesse()  # Lista delle commesse
            data = [{"ID_Commessa": c.ID_Commessa, "Nome": c.Nome} for c in commesse]
            return JSONResponse(content=data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Errore nel recuperare le commesse: {str(e)}")

    def get_commessa_by_filter(self, title: str, db: Session = Depends(get_db)):
        try:
            commessa_service = CommessaService(db)
            commesse = commessa_service.search_commesse(title)  # Cerca commesse per titolo
            data = [{"ID_Commessa": c.ID_Commessa, "Nome": c.Nome} for c in commesse]
            return JSONResponse(content=data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Errore nella ricerca delle commesse: {str(e)}")

    def create_commessa(self, commessa: str, db: Session = Depends(get_db)):
        try:
            commessa_service = CommessaService(db)
            nuova = commessa_service.add_commessa(commessa)  # Crea una nuova commessa
            return {"message": "Commessa creata con successo", "id": nuova.ID_Commessa}
        except Exception as e:
            db.rollback()  # Rollback della transazione in caso d'errore
            raise HTTPException(status_code=400, detail=f"Errore nella creazione della commessa: {str(e)}")

    async def upload_file(
        self,
        commessa: str,
        categoria: str,
        file: UploadFile = File(...)
    ):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        temp_file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        # Salva il file temporaneamente
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        try:
            # Formattazione e manipolazione del file CSV
            formatter = formattatore_csv(
                temp_file_path,
                ['Data\\Ora TX', 'Data\\Ora RX', 'Data\\Ora inizio'],
                commessa
            )
            formatter.converti_date()
            formatter.aggiungi_campo()
            formatter.esporta_file()

            formatted_file_path = formatter.get_url_destinazione()

            return FileResponse(
                formatted_file_path,
                media_type='application/octet-stream',
                filename=os.path.basename(formatted_file_path)
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Errore nel caricare o formattare il file: {str(e)}")
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
