from fastapi import FastAPI, HTTPException, Depends, status
import uvicorn
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


app = FastAPI()

token_CalculScore = "AHshhwdfdsfgxhczcrfkrfdgsgvfkfnvrepdazde"
securite = HTTPBearer()


@app.post("/calculate_credit_score/")
async def calculate_credit_score(debts, late_payments, bankruptcy, credentials: HTTPAuthorizationCredentials = Depends(securite)):
    if credentials.credentials != token_CalculScore:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token"
        )
    else:
        print("Success authentication token")

    credit_score = 0

    debts_weight = 0.4
    late_payments_weight = 0.3
    bankruptcy_weight = 0.3

    credit_score = int((1 - int(debts) / 10000) * debts_weight * 100 +
                       (1 - int(late_payments) / 10) * late_payments_weight * 100 +
                       (1 - int(bankruptcy)) * bankruptcy_weight * 100)

    credit_score = max(0, min(100, credit_score))

    return credit_score


if __name__ == '__main__':

    uvicorn.run(app, host="localhost", port=8003)