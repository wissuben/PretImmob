import time
from urllib.parse import urlencode

from fastapi import FastAPI, Form, UploadFile
from fastapi.params import File

from pydantic import BaseModel
import shutil
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from services.authentification import authenticate_user
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="../interface"), name="static")
class UserCredentials(BaseModel):
    id_client: str
    password: str

@app.get("/", response_class=FileResponse)
async def auth(error: str = None):
    # Construct the URL with query parameters
    url_with_query = "../interface/authentification.html"
    if error:
        url_with_query += "?" + urlencode({"error": error})

    # Serve the file with FileResponse
    return FileResponse(url_with_query)



# Route pour gérer la requête POST du formulaire d'authentification
@app.post("/login", response_class=FileResponse)
async def login(id_client: str = Form(...), password: str = Form(...)):
    # Vérifiez les informations d'authentification ici
    if authenticate_user(id_client, password):
        token = ""
        file_url = f"../interface/upload_file.html"
        return FileResponse(file_url)
    else:
        # Récupérer le message d'erreur de la requête POST
        error = "Échec de l'authentification. Veuillez vérifier vos identifiants."
        # Rediriger vers la route "/" avec l'erreur en paramètre GET
        return await auth(error=error)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Spécifiez le chemin où vous souhaitez enregistrer le fichier
    save_path = "../incoming_files/"

    # Ouvrez le fichier en mode binaire pour l'écriture
    with open(save_path + file.filename, "wb") as buffer:
        # Copiez les données du fichier téléchargé dans le fichier sur le serveur
        shutil.copyfileobj(file.file, buffer)

    file_url = f"../output/result.html"
    time.sleep(10)
    return FileResponse(file_url)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
