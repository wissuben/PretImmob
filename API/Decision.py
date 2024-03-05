import logging
import sys
import re
import json
import uuid
import xml.etree.ElementTree as ET
import os
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn



# solvabilité en réponse on justifie pq (score + historique financier + loan_amount)
app = FastAPI()
securite = HTTPBearer()

token_secret = "AHshhxhczxdfghjkjhgfdfghjkhgf"

headers = {
    'Content-Type': 'application/json',
    'Authorization' : f"Bearer {token_secret}"
}
@app.post("/decision/")
async def decision(InspectionResult, ComplianceResult, solvabilité, credentials: HTTPAuthorizationCredentials = Depends(securite)):
    if credentials.credentials != token_secret:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token"
        )
    else:
        print("Success authentication token")
    if InspectionResult == "Inspection virtuelle réussie" and ComplianceResult == "Conforme aux normes légales et réglementaires" and solvabilité == "Solvable":
        resultat = "APPROBATION DU PRÊT"
    else:
        resultat = "REFUS"
    return resultat



if __name__ == '__main__':

    uvicorn.run(app, host="localhost", port=8005)