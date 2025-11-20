# Project Title
UV + FastAPI + Streamlit Banking System

## Overview
This project implements a simple banking system demonstrating the integration of a FastAPI backend for core banking logic and a Streamlit frontend for the user interface. It includes functionalities for user authentication, depositing funds, and transferring money between accounts. Data persistence is handled via a local `database.json` file.

## How to Use With Gemini-CLI
This section provides instructions on how to interact with this project using the Gemini-CLI, enabling easy regeneration, bug fixing, and feature extensions.

### Initial Setup
1.  **Clone the repository:** (If applicable)
    ```bash
    git clone <repository_url>
    cd <project_directory>
    ```
2.  **Initialize UV project:**
    ```bash
    uv init
    uv venv
    uv add fastapi uvicorn streamlit python-requests
    ```
    *(Note: `python-requests` is used by the Streamlit frontend to communicate with FastAPI.)*

### Prompts to Regenerate Backend Files
If you need to regenerate or modify any specific backend file, you can provide the following types of prompts to the Gemini-CLI:

*   **Regenerate `backend/bank.py`:**
    ```
    Generate backend/bank.py. This file will manage reading/writing database.json. Implement: load_db(), save_db(data), authenticate(name, pin_number), deposit(name, amount), transfer(sender_name, receiver_name, amount), get_balance(name). Store users in database.json in this format: {"users": [{"name": "Ali", "pin_number": "1234", "bank_balance": 5000}]}. All updates must persist to JSON. Add proper error handling. Write full code.
    ```
*   **Regenerate `backend/authenticate_endpoint.py`:**
    ```
    Generate backend/authenticate_endpoint.py using FastAPI. Create: router = APIRouter(), POST /authenticate. Inputs: name: str, pin_number: str. Process: Use authenticate() from bank.py. Return: authenticated: True/False, bank_balance (on success), message (on failure). Write full code.
    ```
*   **Regenerate `backend/deposit_endpoint.py`:**
    ```
    Generate backend/deposit_endpoint.py. Create a FastAPI router: POST /deposit. Inputs: name: str, amount: float. Process: Load user from database.json, Update bank_balance, Save updated JSON. Return: message, updated balance. Write complete working code.
    ```
*   **Regenerate `backend/transfer_endpoint.py`:**
    ```
    Generate backend/transfer_endpoint.py. Create POST /bank-transfer. Inputs: sender_name, sender_pin_number, receiver_name, amount. Process: 1. Authenticate sender, 2. Deduct amount, 3. Add amount to receiver, 4. Save database.json. Return: message, sender_new_balance, receiver_new_balance. Write full code using the bank.py functions.
    ```
*   **Regenerate `backend/main.py`:**
    ```
    Create backend/main.py. Requirements: Initialize FastAPI(), Include routers: authenticate_endpoint.router, deposit_endpoint.router, transfer_endpoint.router. Make sure the app runs using: uv run uvicorn backend.main:app --reload. Write complete code.
    ```

### Prompts to Regenerate Streamlit UI
*   **Regenerate `frontend/app.py`:**
    ```
    Generate frontend/app.py using Streamlit. The app should have 3 sections: 1. Authentication (Inputs: name, pin, POST to /authenticate, Save session_state["name"], Display balance). 2. Deposit (Input: amount, POST to /deposit, Display updated balance). 3. Bank Transfer (sender_name auto-filled from session, inputs: receiver_name, amount, POST to /bank-transfer, After transfer, auto-call /authenticate for the receiver, Display receiver updated balance). Use python requests to call FastAPI endpoints. Write full code.
    ```

### Prompts to Fix Bugs
When encountering a bug, describe the issue clearly to the Gemini-CLI. For example:
*   ```
    The deposit function in backend/bank.py is not correctly updating the balance when the user name is cased differently (e.g., "ali" vs "Ali"). Please fix this.
    ```
*   ```
    The frontend/app.py is not displaying the correct error message when the backend transfer fails due to insufficient funds. Update the error handling to show the specific error message from the API.
    ```

### Prompts to Extend Features
To add new features, specify the desired functionality:
*   ```
    Add a new endpoint to backend/main.py and backend/balance_endpoint.py that allows users to check their balance using a GET request and their name as a query parameter. Update frontend/app.py to include a "Check Balance" button.
    ```
*   ```
    Implement a transaction history feature. Modify backend/bank.py to store transaction logs (deposits, transfers) in database.json and create a new FastAPI endpoint to retrieve them. Update frontend/app.py to display this history.
    ```

## Developer Guide

### How FastAPI Endpoints Work
The backend is built with FastAPI, a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.

*   **`backend/main.py`**: This is the main entry point for the FastAPI application. It initializes the `FastAPI` app and includes routers from other endpoint files.
*   **`backend/bank.py`**: Contains the core business logic for banking operations (authentication, deposit, transfer, balance retrieval) and handles reading/writing to `database.json`. It's designed to be a reusable module.
*   **`backend/*_endpoint.py`**: Files like `authenticate_endpoint.py`, `deposit_endpoint.py`, and `transfer_endpoint.py` define specific API endpoints using `APIRouter`. Each endpoint handles HTTP requests, validates input using Pydantic models, calls the appropriate functions in `bank.py`, and returns JSON responses. Error handling is managed using `HTTPException` for client-side errors and general `Exception` for unexpected server issues.

### How Streamlit UI Interacts with API
The frontend is built with Streamlit, a framework for creating web applications for machine learning and data science. It interacts with the FastAPI backend using the `requests` library.

*   **`frontend/app.py`**: This is the main Streamlit application.
    *   It uses `st.session_state` to maintain the user's login status and current balance across reruns.
    *   HTTP POST requests are sent to the FastAPI endpoints (e.g., `/api/v1/authenticate`, `/api/v1/deposit`, `/api/v1/bank-transfer`) with JSON payloads.
    *   Responses from the backend are parsed (JSON) and used to update the UI or `st.session_state`.
    *   `st.text_input`, `st.number_input`, and `st.button` are used for user input and actions.
    *   `st.success`, `st.error`, and `st.info` are used to provide feedback to the user.
    *   `st.rerun()` is used to force a re-render of the Streamlit app after state changes or successful API calls to reflect updated data.

## Run Instructions (UV)

To run the full application:

1.  **Start the FastAPI Backend:**
    Open your terminal in the project root directory and run:
    ```bash
    uv run uvicorn backend.main:app --reload
    ```
    This will start the FastAPI server, typically on `http://127.0.0.1:8000`. The `--reload` flag enables auto-reloading of the server on code changes.

2.  **Start the Streamlit Frontend:**
    Open a **new** terminal (keep the backend running in the first one) in the project root directory and run:
    ```bash
    streamlit run frontend/app.py
    ```
    This will launch the Streamlit application in your web browser, typically on `http://localhost:8501`.

## Future Enhancements
*   **Gemini-powered fraud detection**: Integrate AI/ML models (potentially using Gemini) to detect suspicious transaction patterns.
*   **AI notifications**: Implement intelligent notification systems for unusual account activity or financial advice.
*   **Multi-user dashboard**: Develop a more sophisticated dashboard allowing users to view detailed transaction history, statements, and manage account settings.
*   **Database integration**: Replace `database.json` with a proper relational database (e.g., SQLite, PostgreSQL) for better scalability and data integrity.
*   **User registration**: Enhance the authentication process to include a user registration flow.
*   **Withdrawal functionality**: Add an endpoint and UI for withdrawing funds.
*   **Admin panel**: Create an administrative interface for managing users and accounts.

