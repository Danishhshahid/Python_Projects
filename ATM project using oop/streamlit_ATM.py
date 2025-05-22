import streamlit as st
import time
from abc import ABC, abstractmethod

# Abstract base class for accounts
class AccountInterface(ABC):
    @abstractmethod
    def authenticate(self, pin):
        pass

    @abstractmethod
    def get_balance(self):
        pass

    @abstractmethod
    def deposit_amount(self, amount):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass

    @abstractmethod
    def change_pin(self, current_pin, new_pin):
        pass

    @abstractmethod
    def atm_menu(self):
        pass

# Base bank account class
class bankAccount(AccountInterface):
    def __init__(self, owner, balance, pin):
        self.__owner = owner
        self.__balance = balance
        self.__pin = pin
        self.__authenticated = False

    def authenticate(self, entered_pin):
        if entered_pin == self.__pin:
            self.__authenticated = True
            return f"Login successful! Welcome, {self.__owner}"
        else:
            self.__authenticated = False
            return "Invalid PIN"

    def get_balance(self):
        if self.__authenticated:
            return f"Your balance is {self.__balance}"
        else:
            return "Please login first."

    def deposit_amount(self, amount):
        if self.__authenticated:
            if amount > 0:
                self.__balance += amount
                return f"Amount {amount} deposited successfully. Current balance: {self.__balance}"
            else:
                return "Invalid deposit amount."
        else:
            return "Please login first."

    def withdraw(self, amount):
        if self.__authenticated:
            if amount > 0 and amount <= self.__balance:
                self.__balance -= amount
                return f"Amount {amount} withdrawn successfully. Remaining balance: {self.__balance}"
            else:
                return "Insufficient balance or invalid amount."
        else:
            return "Please login first."

    def change_pin(self, current_pin, new_pin):
        if self.__authenticated:
            if current_pin == self.__pin:
                self.__pin = new_pin
                return "PIN changed successfully."
            else:
                return "Invalid current PIN."
        else:
            return "Please login first."

    def atm_menu(self):
        pass

# Student account class with withdrawal limit
class studentAccount(bankAccount):
    def withdraw(self, amount):
        if self._bankAccount__authenticated:
            if amount > 10000:
                return "Withdrawal limit exceeded. Max limit is 10,000."
            elif 0 < amount <= self._bankAccount__balance:
                self._bankAccount__balance -= amount
                return "Withdrawal successful!"
            else:
                return "Insufficient balance or invalid amount."
        else:
            return "Please login first."

# Streamlit application
st.title("🏧 Welcome to the ATM Machine")
st.markdown("---")

# Initialize session state
if "accounts" not in st.session_state:
    st.session_state.accounts = {
        "regular": bankAccount("Danish", 3000, 12345),
        "student": studentAccount("Student Shoukat", 4000, 123456)
    }

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "show_menu" not in st.session_state:
    st.session_state.show_menu = False

if "selected_action" not in st.session_state:
    st.session_state.selected_action = None

if "selected_account_key" not in st.session_state:
    st.session_state.selected_account_key = None

# Login section
if not st.session_state.authenticated:
    st.header("🔐 Login")
    account_options = list(st.session_state.accounts.keys())
    selected_account = st.selectbox("Choose Account Type", account_options)
    st.session_state.selected_account_key = selected_account
    account = st.session_state.accounts[selected_account]
    pin_input = st.text_input("Enter your PIN:", type="password")
    if st.button("Login"):
        if pin_input:
            try:
                pin = int(pin_input)
                message = account.authenticate(pin)
                if "successful" in message.lower():
                    st.session_state.authenticated = True
                    st.session_state.show_menu = False
                    st.success(message)
                    time.sleep(2)  # 2-minute delay
                    st.session_state.show_menu = True
                    st.rerun()
                else:
                    st.error(message)
            except ValueError:
                st.error("PIN must be numeric.")
        else:
            st.error("Please enter your PIN.")

# Authenticated state
if st.session_state.authenticated and st.session_state.show_menu:
    account = st.session_state.accounts[st.session_state.selected_account_key]
    with st.sidebar:
        st.title("💳 ATM Menu")
        if st.button("💰 Check Balance"):
            st.session_state.selected_action = "check_balance"
        if st.button("➕ Deposit"):
            st.session_state.selected_action = "deposit"
        if st.button("➖ Withdraw"):
            st.session_state.selected_action = "withdraw"
        if st.button("🔑 Change PIN"):
            st.session_state.selected_action = "change_pin"
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.show_menu = False
            st.session_state.selected_action = None
            st.rerun()

    # Main area
    # st.markdown("---")
    if st.session_state.selected_action is None:
        st.write("Please select an action from the sidebar.")
    elif st.session_state.selected_action == "check_balance":
        st.info(account.get_balance())
    elif st.session_state.selected_action == "deposit":
        st.markdown("### Deposit Money")
        amount = st.number_input("Enter amount to deposit:", value=None, format="%.2f", key="deposit_amount")
        if st.button("Confirm Deposit"):
            if amount is not None and amount > 0:
                result = account.deposit_amount(amount)
                st.success(result)
                st.session_state.selected_action = None
            else:
                st.error("Please enter a valid amount.")
    elif st.session_state.selected_action == "withdraw":
        st.markdown("### Withdraw Money")
        amount = st.number_input("Enter amount to withdraw:", value=None, format="%.2f", key="withdraw_amount")
        if st.button("Confirm Withdraw"):
            if amount is not None and amount > 0:
                result = account.withdraw(amount)
                st.success(result)
                st.session_state.selected_action = None
            else:
                st.error("Please enter a valid amount.")
    elif st.session_state.selected_action == "change_pin":
        st.markdown("### Change PIN")
        current_pin = st.text_input("Enter current PIN:", type="password", key="current_pin")
        new_pin = st.text_input("Enter new PIN:", type="password", key="new_pin")
        if st.button("Confirm Change PIN"):
            if current_pin and new_pin:
                try:
                    current_pin = int(current_pin)
                    new_pin = int(new_pin)
                    result = account.change_pin(current_pin, new_pin)
                    st.success(result)
                    st.session_state.selected_action = None
                except ValueError:
                    st.error("PIN must be numeric.")
            else:
                st.error("Please enter both current and new PIN.")