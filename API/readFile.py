import logging
import re
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from db_services.demande_pret import insert_demande_pret


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
                'nom_client': r"je m'appelle (\w+ \w+),",
                'adresse': r"je vis au (\d+ [\w\s]+).",
                'email': r"par mail : (.+@.+\..+)",
                'num_de_tel': r"me contacter : \+(\d+)",
                'montant_pret_demande': r"pret de (\d+€)",
                'duree_pret': r"pour (\d+) ans",
                'revenu_mensuel': r"je gagne (\d+€)",
                'depenses_mensuelles': r"depenses environ (\d+€)",
            }

            extracted_info = {}

            pattern_description = r"(jardin|vue sur mer|calme|[0-9] ?chambre[s]?|[0-9] ?piscine[s]?|[0-9] ?salle[s] de bain[s]?|[0-9] ?jardin[s]?|[0-9]+m²)"

            # Trouver toutes les correspondances de la description de la propriété
            matches = re.findall(pattern_description, content, re.IGNORECASE)

            # Créer une seule chaîne de caractères à partir des correspondances
            description_complete = ",".join(matches)
            extracted_info["description_de_propriete"] = description_complete
            extracted_info["statut_demande"] = "pending"


            for category, pattern in patterns.items():
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    extracted_info[category] = match.group(1)
            print(extracted_info)
            response = insert_demande_pret(extracted_info)
            if response != -1:
                print("Demande insérée avec succès")
                return {"id_demande_pret": response}
            else:
                return {"error": "Une erreur s'est produite lors de l'insertion de la demande de prêt.","dict": extracted_info}


    except FileNotFoundError:
        logging.exception(f"File not found: {file_name}")
        return {"error": f"Le fichier '{file_name}' est introuvable."}
    except Exception as e:
        logging.exception(f"An error occurred: {str(e)}")
        return {"error": f"Une erreur s'est produite : {str(e)}"}


if __name__ == '__main__':

    uvicorn.run(app, host="localhost", port=8009)
