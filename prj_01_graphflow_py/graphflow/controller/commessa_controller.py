from fastapi import Form, File, Depends, HTTPException, UploadFile, APIRouter, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.orm import Session
from database.database import get_db
from services.auth_service import get_current_user
from services.commessa_service import CommessaService
from services.micromissioni_service import MicroMissioniService
from services.allarmi_service import AllarmiService
from util.csv_utils import carica_e_filtra_csv_micromissioni, carica_e_filtra_csv_allarmi
import shutil
import os
import jwt
import time
import logging
from dotenv import load_dotenv
from database.database import SessionLocal
load_dotenv()

# ------------------ CONFIG ------------------
METABASE_SITE_URL = os.getenv("METABASE_SITE_URL")
METABASE_SECRET_KEY = os.getenv("METABASE_SECRET_KEY")
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")

# Logging configurato
logger = logging.getLogger("commessa_controller")
logging.basicConfig(level=logging.INFO)

# ------------------ FUNZIONE IFRAME ------------------
def genera_metabase_iframe(element_id: int, commessa: str):
    try:
        if not METABASE_SECRET_KEY or not METABASE_SITE_URL:
            raise ValueError("Variabili METABASE mancanti")
        
        payload = {
            "resource": {"dashboard": element_id},
            "params": {"job_order": [commessa]},
            "exp": round(time.time()) + (60 * 60 * 24)
        }
        token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")
        url = f"{METABASE_SITE_URL}/embed/dashboard/{token}#bordered=true&titled=true"
        return url

    except Exception as e:
        logger.exception("Errore genera_metabase_iframe")
        raise HTTPException(status_code=500, detail=f"Errore nella generazione iframe: {str(e)}")

# ------------------ CONTROLLER ------------------
class CommessaController:
    def __init__(self):
        self.router = APIRouter(
            prefix="/api/commessa",
            tags=["Commesse"],
            dependencies=[Depends(get_current_user)]
        )
        self._add_routes()

    def _add_routes(self):
        self.router.get("/all")(self.get_all_commesse)
        self.router.get("/{commessa}/grafico")(self.get_grafico_commessa)
        self.router.get("/{commessa}")(self.get_commessa_by_nome)
        self.router.get("/search/{title}")(self.get_commessa_by_filter)
        self.router.post("/create")(self.create_commessa)
        self.router.post("/{commessa}/{categoria}/upload")(self.upload_file)

    # ------------------ GET COMMESSE ------------------
    def get_all_commesse(self, db: Session = Depends(get_db)):
        try:
            commessa_service = CommessaService(db)
            commesse = commessa_service.list_commesse()
            data = [{"ID_Commessa": c.ID_Commessa, "Nome": c.Nome} for c in commesse]
            return JSONResponse(content=data)
        except Exception as e:
            logger.exception("Errore get_all_commesse")
            raise HTTPException(status_code=400, detail=str(e))

    def get_commessa_by_nome(self, commessa: int, db: Session = Depends(get_db)):
        try:
            commessa_service = CommessaService(db)
            commessa_obj = commessa_service.get_commessa_by_id(commessa)
            if not commessa_obj:
                raise HTTPException(status_code=404, detail="Commessa non trovata")
            return {"ID_Commessa": commessa_obj.ID_Commessa, "Nome": commessa_obj.Nome}
        except Exception as e:
            logger.exception("Errore get_commessa_by_nome")
            raise HTTPException(status_code=400, detail=str(e))

    def get_commessa_by_filter(self, title: str, db: Session = Depends(get_db)):
        try:
            commessa_service = CommessaService(db)
            commesse = commessa_service.search_commesse(title)
            data = [{"ID_Commessa": c.ID_Commessa, "Nome": c.Nome} for c in commesse]
            return JSONResponse(content=data)
        except Exception as e:
            logger.exception("Errore get_commessa_by_filter")
            raise HTTPException(status_code=400, detail=str(e))

    # ------------------ CREATE COMMESSA ------------------
    def create_commessa(
        self,
        commessa: str = Form(...),
        descrizione: str = Form(None),
        foto: UploadFile = File(None),
        db: Session = Depends(get_db)
    ):
        try:
            commessa_service = CommessaService(db)
            nuova = commessa_service.add_commessa(commessa)
            return {"message": "Commessa creata con successo", "id": nuova.ID_Commessa}
        except Exception as e:
            db.rollback()
            logger.exception("Errore create_commessa")
            raise HTTPException(status_code=400, detail=str(e))

    # ------------------ GET GRAFICO ------------------
    async def get_grafico_commessa(self, commessa: int, db: Session = Depends(get_db)):
        try:
            commessa_service = CommessaService(db)
            commessa_data = await run_in_threadpool(commessa_service.get_commessa_by_id, commessa)
            if not commessa_data:
                raise HTTPException(status_code=404, detail="Commessa non trovata")
            
            iframe_url = await run_in_threadpool(genera_metabase_iframe, 130, commessa_data.Nome)
            iframe_html = f'<iframe src="{iframe_url}" frameborder="0" width="100%" height="900" allowtransparency></iframe>'
            return HTMLResponse(content=iframe_html)

        except HTTPException:
            raise
        except Exception as e:
            logger.exception("Errore get_grafico_commessa")
            raise HTTPException(status_code=500, detail=str(e))

    # ------------------ UPLOAD FILE ------------------
    async def upload_file(self, commessa: str, categoria: str, file: UploadFile = File(...)):
        db = SessionLocal()
        try:
            temp_file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            await run_in_threadpool(shutil.copyfileobj, file.file, open(temp_file_path, "wb"))

            if categoria == "micromissioni":
                df = await run_in_threadpool(carica_e_filtra_csv_micromissioni, temp_file_path)
                micro_service = MicroMissioniService(db)
                await run_in_threadpool(micro_service.carica_micromissioni, int(commessa), df)

            elif categoria == "allarmi":
                df = await run_in_threadpool(carica_e_filtra_csv_allarmi, temp_file_path)
                allarmi_service = AllarmiService(db)
                await run_in_threadpool(allarmi_service.carica_allarmi, int(commessa), df)

            else:
                raise HTTPException(status_code=400, detail=f"Categoria '{categoria}' non supportata")

            return JSONResponse(content={"message": f"Dati '{categoria}' inseriti con successo per commessa {commessa}."})

        except Exception as e:
            db.rollback()
            logger.exception("Errore upload_file")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            db.close()
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)