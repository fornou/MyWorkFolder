from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

from services.auth_service import get_current_user

class MVCController:
    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get("/", response_class=HTMLResponse)(self.serve_commesse)
        self.router.get("/commesse", response_class=HTMLResponse)(self.serve_commesse)
        self.router.get("/commesse/{commessa}", response_class=HTMLResponse)(self.serve_commessa)
        self.router.get("/create-new-commessa", response_class=HTMLResponse)(self.serve_form_commessa)
        self.router.get("/commessa/{commessa}/{categoria}/upload-csv", response_class=HTMLResponse)(self.serve_form_upload_csv)
        self.router.get("/auth", response_class=HTMLResponse)(self.serve_auth)

    async def serve_commesse(self):
        return self._serve_html("resources/static/commesse_all.html")

    async def serve_commessa(self):
        return self._serve_html("resources/static/commessa.html")

    async def serve_form_commessa(self):
        return self._serve_html("resources/static/form_commessa.html")

    async def serve_form_upload_csv(self):
        return self._serve_html("resources/static/form_upload_csv.html")
    
    async def serve_auth(self):
        return self._serve_html("resources/static/auth.html")
    
    def _serve_html(self, path: str):
        try:
            with open(path, "r", encoding="utf-8") as file:
                return HTMLResponse(content=file.read())
        except FileNotFoundError:
            with open("resources/static/404.html", "r", encoding="utf-8") as file_404:
                return HTMLResponse(content=file_404.read(), status_code=404)

