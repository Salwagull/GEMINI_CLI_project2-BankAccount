from vercel_kv import kv
from typing import Dict, Any

# Initial data to populate the database if it's empty
INITIAL_DB = {
    "users": [
        {"name": "Ali", "pin_number": "1234", "bank_balance": 5000},
        {"name": "Mona", "pin_number": "5678", "bank_balance": 7500},
        {"name": "Saif", "pin_number": "9876", "bank_balance": 3200},
    ]
}

def load_db() -> Dict[str, Any]:
    """Reads the database from Vercel KV or initializes it."""
    db = kv.get("database")
    if db is None:
        # If the db doesn't exist, initialize it with default data
        kv.set("database", INITIAL_DB)
        return INITIAL_DB
    # The data from KV is already a dictionary
    return db

def save_db(data: Dict[str, Any]) -> None:
    """Saves the given data to Vercel KV."""
    kv.set("database", data)

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
            # Ensure balance is treated as a number
            user["bank_balance"] = float(user.get("bank_balance", 0)) + amount
            user_found = True
            break
    
    if not user_found:
        raise ValueError("Deposit failed: User not found.")

    save_db(db)
    # Re-fetch user to get the updated balance accurately
    updated_user = _find_user(name)
    return updated_user["bank_balance"]


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

    # Ensure balances are numeric
    sender["bank_balance"] = float(sender.get("bank_balance", 0))
    receiver["bank_balance"] = float(receiver.get("bank_balance", 0))

    if sender["bank_balance"] < amount:
        raise ValueError("Transfer failed: Insufficient funds.")

    sender["bank_balance"] -= amount
    receiver["bank_balance"] += amount

    save_db(db)

def get_all_user_names() -> list[str]:
    """Returns a list of all user names from the database."""
    db = load_db()
    # Handle case where db might not have 'users' key
    return [user["name"] for user in db.get("users", [])]