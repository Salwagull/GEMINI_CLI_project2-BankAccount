import json
from typing import Dict, Any

DATABASE_FILE = "database.json"

def load_db() -> Dict[str, Any]:
    """Reads the database file and returns its content."""
    try:
        with open(DATABASE_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or is empty/corrupt, return a default structure
        return {"users": []}

def save_db(data: Dict[str, Any]) -> None:
    """Saves the given data to the database file."""
    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def _find_user(name: str):
    """Helper function to find a user by name."""
    db = load_db()
    for user in db.get("users", []):
        if user["name"].lower() == name.lower():
            return user
    return None

def authenticate(name: str, pin_number: str) -> bool:
    """Authenticates a user based on name and PIN."""
    user = _find_user(name)
    if not user:
        raise ValueError("Authentication failed: User not found.")
    if user["pin_number"] != pin_number:
        raise ValueError("Authentication failed: Invalid PIN.")
    return True

def get_balance(name: str) -> float:
    """Gets the bank balance for a specific user."""
    user = _find_user(name)
    if not user:
        raise ValueError("Cannot get balance: User not found.")
    return user["bank_balance"]

def deposit(name: str, amount: float) -> float:
    """Deposits a given amount into a user's account."""
    if amount <= 0:
        raise ValueError("Deposit amount must be positive.")

    db = load_db()
    user_found = False
    for user in db.get("users", []):
        if user["name"].lower() == name.lower():
            user["bank_balance"] += amount
            user_found = True
            break
    
    if not user_found:
        raise ValueError("Deposit failed: User not found.")

    save_db(db)
    return get_balance(name)

def transfer(sender_name: str, receiver_name: str, amount: float) -> None:
    """Transfers a given amount from one user to another."""
    if amount <= 0:
        raise ValueError("Transfer amount must be positive.")
    
    if sender_name.lower() == receiver_name.lower():
        raise ValueError("Sender and receiver cannot be the same person.")

    db = load_db()
    sender = None
    receiver = None

    for user in db.get("users", []):
        if user["name"].lower() == sender_name.lower():
            sender = user
        if user["name"].lower() == receiver_name.lower():
            receiver = user

    if not sender:
        raise ValueError("Transfer failed: Sender not found.")
    if not receiver:
        raise ValueError("Transfer failed: Receiver not found.")

    if sender["bank_balance"] < amount:
        raise ValueError("Transfer failed: Insufficient funds.")

    sender["bank_balance"] -= amount
    receiver["bank_balance"] += amount

    save_db(db)

def get_all_user_names() -> list[str]:
    """Returns a list of all user names from the database."""
    db = load_db()
    return [user["name"] for user in db.get("users", [])]
