from fastapi import APIRouter, HTTPException
from . import bank

router = APIRouter()

@router.get("/users")
async def get_users():
    """
    Retrieves a list of all user names.
    """
    try:
        user_names = bank.get_all_user_names()
        return {"users": user_names}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

