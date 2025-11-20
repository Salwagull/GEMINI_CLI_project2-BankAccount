from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from . import bank

router = APIRouter()

class TransferRequest(BaseModel):
    sender_name: str
    sender_pin_number: str
    receiver_name: str
    amount: float

@router.post("/bank-transfer")
async def transfer_funds(request: TransferRequest):
    """
    Handles transferring funds from one user to another after authenticating the sender.
    Returns a success message and the new balances for both users, or an error message on failure.
    """
    try:
        # 1. Authenticate sender
        authenticated = bank.authenticate(request.sender_name, request.sender_pin_number)
        if not authenticated:
            # This case is unlikely if bank.authenticate raises ValueError, but included for safety
            raise ValueError("Authentication failed for sender.")

        # 2. Perform the transfer (deducts from sender, adds to receiver)
        bank.transfer(request.sender_name, request.receiver_name, request.amount)
        
        # 3. Get updated balances
        sender_new_balance = bank.get_balance(request.sender_name)
        receiver_new_balance = bank.get_balance(request.receiver_name)

        return {
            "message": "Transfer successful.",
            "sender_new_balance": sender_new_balance,
            "receiver_new_balance": receiver_new_balance
        }
    except ValueError as e:
        # Catches errors from both authenticate() and transfer()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

