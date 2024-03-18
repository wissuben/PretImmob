from fastapi import FastAPI, HTTPException, Form, UploadFile
from fastapi.responses import FileResponse
from fastapi.params import File, Depends
from pydantic import BaseModel
import shutil
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from authentification import authenticate_user
import uvicorn

app = FastAPI()

class UserCredentials(BaseModel):
    id_client: str
    password: str


# Route pour gérer la requête POST du formulaire d'authentification
@app.post("/login", response_class=FileResponse)
async def login(id_client: str = Form(...), password: str = Form(...)):
    # Vérifiez les informations d'authentification ici
    if authenticate_user(id_client, password):
        return FileResponse("../interface/upload_file.html")
    else:
        raise HTTPException(status_code=401,
                            detail="Échec de l'authentification : nom d'utilisateur ou mot de passe incorrect.")


# File upload endpoint
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Spécifiez le chemin où vous souhaitez enregistrer le fichier
    save_path = "../incoming_files/"

    # Ouvrez le fichier en mode binaire pour l'écriture
    with open(save_path + file.filename, "wb") as buffer:
        # Copiez les données du fichier téléchargé dans le fichier sur le serveur
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "message": "Fichier téléchargé avec succès"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
