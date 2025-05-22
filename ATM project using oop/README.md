# ATM System with Streamlit

This is a simple ATM (Automated Teller Machine) system implemented using Python and Streamlit. The application provides basic banking functionalities like checking balance, depositing money, withdrawing money, and changing PIN.

## Features

- User authentication with PIN
- Multiple account types (Regular and Student)
- Check balance
- Deposit money
- Withdraw money (with limits for student accounts)
- Change PIN
- Secure session management

## Installation

1. Clone this repository
2. Create a virtual environment (recommended):
   ```bash
   python -m venv atm_env
   source atm_env/bin/activate  # On Windows: atm_env\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

To run the application locally:

```bash
streamlit run streamlit_ATM.py
```

## Deployment

To deploy this application on Streamlit Cloud:

1. Push your code to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your repository, branch, and main file (streamlit_ATM.py)
6. Click "Deploy"

## Default Accounts

The application comes with two default accounts:

1. Regular Account:
   - Owner: Danish
   - PIN: 12345
   - Initial Balance: 3000

2. Student Account:
   - Owner: Student Shoukat
   - PIN: 123456
   - Initial Balance: 4000
   - Withdrawal Limit: 10,000

## Security Note

This is a demonstration application. In a production environment, you should:
- Use secure password hashing
- Implement proper database storage
- Add additional security measures
- Use environment variables for sensitive data 