from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from . import bank

router = APIRouter()

class AuthRequest(BaseModel):
    name: str
    pin_number: str

@router.post("/authenticate")
async def authenticate_user(request: AuthRequest):
    """
    Authenticates a user with the provided name and PIN number.
    Returns authentication status, bank balance on success, or an error message on failure.
    """
    try:
        # Authenticate the user
        authenticated = bank.authenticate(request.name, request.pin_number)
        
        if authenticated:
            # If authenticated, get the bank balance
            balance = bank.get_balance(request.name)
            return {"authenticated": True, "bank_balance": balance}
        else:
            # This path should ideally not be hit if bank.authenticate raises ValueError
            return {"authenticated": False, "message": "Authentication failed: Unknown reason."}
    except ValueError as e:
        # Catch specific authentication errors from bank.py
        return {"authenticated": False, "message": str(e)}
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

