
from fastapi import FastAPI, HTTPException, Depends, status
import uvicorn
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


securite = HTTPBearer()

app = FastAPI()

token_secret = "AHshhsdfghjklkjhgfdsdfghjkvrepdazdede"

headers = {
    'Content-Type': 'application/json',
    'Authorization' : f"Bearer {token_secret}"
}

class InspectionInfo:
    def __init__(self, InspectionVirtuelle, InspectionSurPlace):
        self.InspectionVirtuelle = InspectionVirtuelle
        self.InspectionSurPlace = InspectionSurPlace


class LegalCompliance:
    def __init__(self, LitigesFonciersEnCours, ConformiteReglementsBatiment, EligibilitePretImmobilier):
        self.LitigesFonciersEnCours = LitigesFonciersEnCours
        self.ConformiteReglementsBatiment = ConformiteReglementsBatiment
        self.EligibilitePretImmobilier = EligibilitePretImmobilier



class EvaluationResult:
    def __init__(self, PropertyValuation, InspectionResult, ComplianceResult):
        self.PropertyValuation = PropertyValuation
        self.InspectionResult = InspectionResult
        self.ComplianceResult = ComplianceResult




@app.post("/EvaluateProperty/")
async def EvaluateProperty(property_description, credentials: HTTPAuthorizationCredentials = Depends(securite)):

    if credentials.credentials != token_secret:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token"
        )
    else:
        print("Success authentication token")

    # Initialiser la valeur de base de la propriété
    property_valuation = 300000.00
    description = property_description
    print(description)

    # Analyse de la description pour extraire les détails
    if "jardin" in description:
        property_valuation += 1000
    if "piscine" in description:
        property_valuation += 900
    if "calme" in description:
        property_valuation += 2000

    # Simuler l'évaluation de l'inspection et de la conformité légale
    inspection_result = "Inspection virtuelle réussie"
    compliance_result = "Conforme aux normes légales et réglementaires"

    evaluation_result = EvaluationResult(PropertyValuation=property_valuation, InspectionResult=inspection_result,
                                         ComplianceResult=compliance_result)

    evaluation_result_json = jsonable_encoder(evaluation_result)

    return JSONResponse(content=evaluation_result_json)


if __name__ == '__main__':

    uvicorn.run(app, host="localhost", port=8008)