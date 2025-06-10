from fastapi import Form, File, Depends, HTTPException, UploadFile, APIRouter
from fastapi.responses import JSONResponse, HTMLResponse
from sqlalchemy.orm import Session
from database.database import get_db
from services.auth_service import get_current_user
from services.commessa_service import CommessaService
import shutil, os
import jwt
import time
from dotenv import load_dotenv
from services.micromissioni_service import MicroMissioniService
from services.allarmi_service import AllarmiService
from util.csv_utils import carica_e_filtra_csv_micromissioni, carica_e_filtra_csv_allarmi
load_dotenv()

METABASE_SITE_URL = os.getenv("METABASE_SITE_URL")
METABASE_SECRET_KEY = os.getenv("METABASE_SECRET_KEY")
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")

def genera_metabase_iframe(element_id: int, commessa: str):
    try:
        payload = {
            "resource": {"dashboard": element_id},
            "params": {"job_order": [commessa]},
            "exp": round(time.time()) + (60 * 60 * 24)  # 1 giorno
        }
        token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")
        return f"{METABASE_SITE_URL}/embed/dashboard/{token}#bordered=true&titled=true"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore: {str(e)}")

class CommessaController:
    def __init__(self):
        self.router = APIRouter(prefix="/api/commessa", tags=["Commesse"], dependencies=[Depends(get_current_user)])
        self._add_routes()

    def _add_routes(self):
        self.router.get("/all")(self.get_all_commesse)
        self.router.get("/{commessa}/grafico")(self.get_grafico_commessa)
        self.router.get("/{commessa}")(self.get_commessa_by_nome)
        self.router.get("/search/{title}")(self.get_commessa_by_filter)
        self.router.post("/create")(self.create_commessa)
        self.router.post("/{commessa}/{categoria}/upload")(self.upload_file)

    def get_grafico_commessa(self, commessa: int, db: Session = Depends(get_db)):
        try:
            commessa_service = CommessaService(db)
            commessa_data = commessa_service.get_commessa_by_id(commessa)

            # Dashboard ID fisso (esempio 130)
            dashboard_id = 130

            iframe_url = genera_metabase_iframe(dashboard_id, commessa_data.Nome)
            iframe_html = f'''
                <iframe src="{iframe_url}" frameborder="0" width="100%" height="600" allowtransparency></iframe>
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
            commesse = commessa_service.list_commesse()
            data = [{"ID_Commessa": c.ID_Commessa, "Nome": c.Nome} for c in commesse]
            return JSONResponse(content=data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Errore nel recuperare le commesse: {str(e)}")

    def get_commessa_by_filter(self, title: str, db: Session = Depends(get_db)):
        try:
            commessa_service = CommessaService(db)
            commesse = commessa_service.search_commesse(title)
            data = [{"ID_Commessa": c.ID_Commessa, "Nome": c.Nome} for c in commesse]
            return JSONResponse(content=data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Errore nella ricerca delle commesse: {str(e)}")

    def create_commessa(self, commessa: str = Form(...), descrizione: str = Form(None), foto: UploadFile = File(None), db: Session = Depends(get_db)):
        try:
            commessa_service = CommessaService(db)
            nuova = commessa_service.add_commessa(commessa)
            return {"message": "Commessa creata con successo", "id": nuova.ID_Commessa}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Errore nella creazione della commessa: {str(e)}")

    async def upload_file(self, commessa: str, categoria: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        temp_file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        try:
            with open(temp_file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            if categoria == "micromissioni":
                df = carica_e_filtra_csv_micromissioni(temp_file_path)
                micro_service = MicroMissioniService(db)
                micro_service.carica_micromissioni(int(commessa), df)

            elif categoria == "allarmi":
                df = carica_e_filtra_csv_allarmi(temp_file_path)
                allarmi_service = AllarmiService(db)
                allarmi_service.carica_allarmi(int(commessa), df)

            else:
                raise HTTPException(status_code=400, detail=f"Categoria '{categoria}' non supportata")

            return JSONResponse(content={"message": f"Dati '{categoria}' inseriti con successo per commessa {commessa}."})

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Errore: {str(e)}")

        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
