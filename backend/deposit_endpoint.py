from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from . import bank

router = APIRouter()

class DepositRequest(BaseModel):
    name: str
    amount: float

@router.post("/deposit")
async def deposit_funds(request: DepositRequest):
    """
    Handles depositing funds into a user's account.
    Returns a success message and the new balance, or an error message on failure.
    """
    try:
        new_balance = bank.deposit(request.name, request.amount)
        return {"message": "Deposit successful.", "new_balance": new_balance}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

