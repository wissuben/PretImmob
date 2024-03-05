import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


app = FastAPI()

token_secret = "AHshhxhczcrfkrfdgsgvfkfnvrepdazdede"
securite = HTTPBearer()


@app.post("/verify_solvency/")
async def verify_solvency(credit_score: float, monthly_expenses: float, loan_amount: float, monthly_income: float, credentials: HTTPAuthorizationCredentials = Depends(securite)):

    if credentials.credentials != token_secret:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token"
        )
    else:
        print("Success authentication token")

    print(credit_score)
    print(monthly_expenses)
    print(monthly_income)
    print(loan_amount)

    if credit_score >= 50 and (monthly_expenses + loan_amount) <= 0.5 * monthly_income:
        return "Solvable"
    else:
        return "Non solvable"

if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8002)
