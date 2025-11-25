import streamlit as st
import requests

# Base URL for the FastAPI backend
BASE_URL = "http://127.0.0.1:8000/api/v1"

@st.cache_data(ttl=30)  # Cache the user list for 30 seconds
def get_user_list():
    """Fetches the list of user names from the backend."""
    try:
        response = requests.get(f"{BASE_URL}/users")
        response.raise_for_status()
        return response.json().get("users", [])
    except requests.exceptions.RequestException:
        return None  # Return None if backend is not available

def login_page():
    """Displays the login page and handles authentication."""
    with st.container(border=True):
        st.header("Login to Your Bank Account")
        user_list = get_user_list()

        if user_list is None:
            st.error(
                "**Failed to connect to the backend.**\n\n"
                "Please ensure the backend server is running and accessible."
            )
            name = st.text_input("Name", key="login_name", disabled=True)
        elif not user_list:
            st.warning("No users found in the database.")
            name = st.text_input("Name", key="login_name", disabled=True)
        else:
            name = st.selectbox("Select Your Name", options=[""] + user_list, key="login_name_select")

        pin = st.text_input("PIN", type="password", key="login_pin")

        if st.button("Login"):
            if not name or not pin:
                st.error("Please select a name and enter your PIN.")
                return

            try:
                response = requests.post(
                    f"{BASE_URL}/authenticate",
                    json={"name": name, "pin_number": pin}
                )
                response.raise_for_status()
                
                data = response.json()
                if data.get("authenticated"):
                    st.session_state["authenticated"] = True
                    st.session_state["name"] = name
                    st.session_state["balance"] = data.get("bank_balance")
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error(data.get("message", "Authentication failed."))
            except requests.exceptions.HTTPError as e:
                st.error(f"Authentication failed: {e.response.json().get('detail', 'Unknown error')}")
            except requests.exceptions.RequestException:
                st.error("Failed to connect to the backend. Please check if the server is running.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

def main_app():
    """Displays the main application interface after login."""
    st.header(f"Welcome, {st.session_state['name']}!")
    st.subheader(f"Your current balance is: ${st.session_state.get('balance', 0):.2f}")

    if st.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    st.markdown("---")

    # --- Deposit Section ---
    with st.expander("💰 Make a Deposit", expanded=True):
        st.subheader("Deposit Funds")
        deposit_amount = st.number_input("Amount to Deposit", min_value=0.01, step=0.01, format="%.2f", key="deposit_amount_input")
        if st.button("Deposit", key="deposit_button"):
            if deposit_amount <= 0:
                st.error("Deposit amount must be a positive number.")
                return

            try:
                response = requests.post(
                    f"{BASE_URL}/deposit",
                    json={"name": st.session_state["name"], "amount": deposit_amount}
                )
                response.raise_for_status()
                data = response.json()
                st.session_state["balance"] = data.get("new_balance")
                st.success(data.get("message"))
                st.rerun()
            except requests.exceptions.HTTPError as e:
                st.error(f"Deposit failed: {e.response.json().get('detail', 'Unknown error')}")
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to the backend: {e}")

    st.markdown("---")

    # --- Bank Transfer Section ---
    with st.expander("💸 Bank Transfer", expanded=True):
        st.subheader("Transfer Funds")
        st.write(f"You are sending from: **{st.session_state['name']}**")
        
        user_list = get_user_list()

        if user_list is None:
            st.warning("Cannot fetch user list. Bank transfers are currently unavailable.")
            return

        receivers_list = [user for user in user_list if user != st.session_state["name"]]

        if not receivers_list:
            st.warning("No other users available to transfer to.")
            return

        receiver_name = st.selectbox("Select Receiver", options=receivers_list, key="receiver_name_select")
        sender_pin = st.text_input("Confirm Your PIN", type="password", key="transfer_pin_input")
        transfer_amount = st.number_input("Amount to Transfer", min_value=0.01, step=0.01, format="%.2f", key="transfer_amount_input")

        if st.button("Transfer", key="transfer_button"):
            if not sender_pin or not receiver_name or transfer_amount <= 0:
                st.warning("Please fill in all transfer details correctly.")
                return
                
            try:
                response = requests.post(
                    f"{BASE_URL}/bank-transfer",
                    json={
                        "sender_name": st.session_state["name"],
                        "sender_pin_number": sender_pin,
                        "receiver_name": receiver_name,
                        "amount": transfer_amount,
                    }
                )
                response.raise_for_status()
                data = response.json()

                st.session_state["balance"] = data.get("sender_new_balance")

                st.success(data.get("message"))
                st.info(f"Your new balance: ${data.get('sender_new_balance'):.2f}")
                st.info(f"Receiver ({receiver_name})'s new balance: ${data.get('receiver_new_balance'):.2f}")

                st.toast("Updating your balance...")
                import time
                time.sleep(2)
                st.rerun()

            except requests.exceptions.HTTPError as e:
                st.error(f"Transfer failed: {e.response.json().get('detail', 'Unknown error')}")
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to the backend: {e}")

def main():
    st.set_page_config(layout="wide", page_title="Gemini Bank")

    # Custom CSS for a modern look with animations and professional font
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&display=swap');
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes slideInUp {
            from { transform: translateY(20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }

        :root {
            --primary-color: #001f3f; /* Navy Blue */
            --secondary-color: #6c757d; /* Gray */
            --success-color: #28a745; /* Green */
            --danger-color: #dc3545; /* Red */
            --warning-color: #ffc107; /* Yellow */
            --info-color: #17a2b8; /* Cyan */
            --dark-color: #343a40; /* Dark Gray */
            --light-color: #f8f9fa; /* Light Gray */
            --text-color: #212529; /* Dark text */
            --background-color: #ffffff; /* White background */
            --card-background: #f8f9fa; /* Light card background */
            --border-color: #ced4da;
            --font-family: 'Montserrat', sans-serif;
        }
        
        body, .stApp {
            font-family: var(--font-family);
            color: var(--text-color);
            background-color: var(--background-color);
        }
        
        /* Main content container styling */
        .main .block-container {
            max-width: 900px;
            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 1rem;
            padding-right: 1rem;
            animation: fadeIn 0.5s ease-in;
        }
        
        /* Hero Section Styling */
        .hero-container {
            background: linear-gradient(135deg, var(--primary-color) 0%, #003366 100%);
            padding: 2rem 1rem;
            color: white;
            text-align: center;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 2rem;
            border-radius: 0.5rem;
            animation: fadeIn 1s ease-in-out;
        }
        .hero-container h2 {
            color: white !important;
            font-size: 2.2rem;
            margin-bottom: 0.8rem;
            animation: slideInUp 0.6s ease-out;
            font-weight: 600;
        }
        .hero-container p {
            font-size: 1rem;
            margin-bottom: 1.5rem;
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
            animation: slideInUp 0.8s ease-out;
        }
        
        /* General Streamlit component styling adjustments */
        h1, h2, h3, h4, h5, h6 {
            font-family: var(--font-family);
        }

        h1 {
            color: var(--dark-color);
            padding: 1rem;
            background-color: var(--light-color);
            border-radius: 0.5rem;
            text-align: center;
            animation: slideInUp 0.5s ease-out;
            font-weight: 600;
        }
        
        h2, h3 {
            color: var(--primary-color);
            font-weight: 600;
        }

        /* Buttons */
        .stButton button {
            background-color: var(--primary-color);
            color: white;
            border-color: var(--primary-color);
            border-radius: 0.5rem;
            padding: 0.75rem 1rem; /* Slightly larger buttons */
            transition: all 0.2s ease-in-out;
            width: 100%;
            animation: slideInUp 0.9s ease-out;
            font-family: var(--font-family);
            font-weight: 600;
            font-size: 1rem;
        }
        .stButton button:hover {
            background-color: #0056b3;
            border-color: #0056b3;
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        }
        .stButton button:active {
            transform: translateY(0);
        }

        /* Input fields */
        .stTextInput, .stNumberInput, .stSelectbox {
             border-radius: 0.5rem;
             border: 1px solid var(--border-color);
             padding: 0.5rem;
             background-color: var(--background-color);
             animation: slideInUp 0.7s ease-out;
        }
        
        /* Customizing Streamlit's expander for sections */
        .streamlit-expanderHeader {
            font-size: 1.2em;
            font-weight: 600;
            background-color: var(--primary-color);
            color: white;
            padding: 0.75rem 1rem;
            border-radius: 0.5rem;
            margin-bottom: 0.5rem;
            transition: background-color 0.3s ease;
        }
        .streamlit-expanderHeader:hover {
            background-color: #0056b3; /* Darker blue on hover */
        }
        .st-expander {
            border: none;
            animation: fadeIn 0.8s ease-in;
        }
        .st-expander > div > div > div {
            border: 1px solid var(--border-color);
            border-top: none;
            border-radius: 0 0 0.5rem 0.5rem;
            padding: 1.5rem;
            background-color: var(--card-background);
        }

        /* Container for main content */
        .st-container {
            border: 1px solid var(--border-color);
            border-radius: 0.5rem;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            background-color: var(--card-background);
            animation: fadeIn 0.6s ease-in;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # --- Hero Section ---
    with st.container():
        st.markdown(
            """
            <div class="hero-container">
                <h2>Manage Your Finances with Ease</h2>
                <p>Experience seamless and secure banking, right at your fingertips. Deposit, transfer, and keep track of your money effortlessly.</p>
            </div>
            """, unsafe_allow_html=True
        )

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        main_app()
    else:
        login_page()

if __name__ == "__main__":
    main()