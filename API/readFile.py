import logging
import sys
import re
import json
import uuid
import xml.etree.ElementTree as ET
import os
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI()
securite = HTTPBearer()


token_secret = "fdfdfdfdfdgrghth"

headers = {
    'Content-Type': 'application/json',
    'Authorization' : f"Bearer {token_secret}"
}
@app.post("/read_file/")
async def read_file(file_name, credentials: HTTPAuthorizationCredentials = Depends(securite)):
    if credentials.credentials != token_secret:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token"
        )
    else:
        print("Success authentication token")
    try:
        with open(file_name, 'r') as file:
            content = file.read()

            # Define patterns for extracting information
            patterns = {
                'Nom_du_Client': r"je m'appelle (\w+ \w+),",
                'Adresse': r"je vis au (\d+ [a-zA-Z\s]+) a ([a-zA-Z]+)\.",
                'Email': r"par mail : (.+@.+\..+)",
                'Numero_de_Telephone': r"me contacter : \+(\d+)",
                'Montant_du_Pret_Demande': r"pret de (\d+€)",
                'Duree_du_Pret': r"pour (\d+) ans",
                'Revenu_mensuel': r"je gagne (\d+€)",
                'Depenses_Mensuelles': r"depenses environ (\d+€)",
            }

            extracted_info = {}

            pattern_description = r"(jardin|vue sur mer|calme|[0-9] ?chambre[s]?|[0-9] ?piscine[s]?|[0-9] ?salle[s] de bain[s]?|[0-9] ?jardin[s]?|[0-9]+m²)"

            # Trouver toutes les correspondances de la description de la propriété
            matches = re.findall(pattern_description, content, re.IGNORECASE)

            # Créer une seule chaîne de caractères à partir des correspondances
            description_complete = ",".join(matches)
            extracted_info["description_de_propriete"] = description_complete

            for category, pattern in patterns.items():
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    extracted_info[category] = match.group(1)

            return extracted_info


    except FileNotFoundError:
        logging.exception(f"File not found: {file_name}")
        return {"error": f"Le fichier '{file_name}' est introuvable."}
    except Exception as e:
        logging.exception(f"An error occurred: {str(e)}")
        return {"error": f"Une erreur s'est produite : {str(e)}"}


if __name__ == '__main__':

    uvicorn.run(app, host="localhost", port=8001)
