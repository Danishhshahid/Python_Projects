import streamlit as st
import re

def check_password_strength(password):
    """
    Evaluate password strength based on various criteria
    Returns a score (0-100) and feedback
    """
    score = 0
    feedback = []
    
    # Check length
    if len(password) == 0:
        return 0, ["Please enter a password"]
    
    if len(password) < 8:
        feedback.append("Password is too short (minimum 8 characters)")
    else:
        score += 20
        if len(password) >= 12:
            score += 10
            
    # Check for uppercase letters
    if re.search(r'[A-Z]', password):
        score += 15
    else:
        feedback.append("Add uppercase letters")
    
    # Check for lowercase letters
    if re.search(r'[a-z]', password):
        score += 15
    else:
        feedback.append("Add lowercase letters")
    
    # Check for numbers
    if re.search(r'\d', password):
        score += 15
    else:
        feedback.append("Add numbers")
    
    # Check for special characters
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 15
    else:
        feedback.append("Add special characters (!@#$%^&*(),.?\":{}|<>)")
    
    # Check for common patterns
    common_patterns = ['123456', 'password', 'qwerty', 'admin']
    if any(pattern in password.lower() for pattern in common_patterns):
        score -= 20
        feedback.append("Avoid common patterns")
    
    # Determine strength category
    if score < 40:
        strength = "Weak"
        color = "red"
    elif score < 70:
        strength = "Moderate"
        color = "orange"
    else:
        strength = "Strong"
        color = "green"
        
    if not feedback:
        feedback.append("Great password!")
        
    return score, feedback, strength, color

def main():
    st.title("Password Strength Meter")
    st.write("Enter a password to check its strength")
    
    password = st.text_input("Password", type="password")
    
    if password:
        score, feedback, strength, color = check_password_strength(password)
        
        # Display strength meter
        st.write(f"Strength: **{strength}**")
        st.progress(score/100)
        
        # Custom color for the strength indicator
        st.markdown(
            f"""
            <style>
            .stProgress > div > div > div > div {{
                background-color: {color};
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )
        
        # Display feedback
        st.subheader("Feedback:")
        for item in feedback:
            st.write(f"- {item}")
            
        # Display score
        st.write(f"Score: {score}/100")
        
        # Password entropy estimation (simplified)
        char_set_size = sum([
            bool(re.search(r'[a-z]', password)) * 26,
            bool(re.search(r'[A-Z]', password)) * 26,
            bool(re.search(r'\d', password)) * 10,
            bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password)) * 30
        ])
        
        if char_set_size > 0:
            entropy = len(password) * (char_set_size.bit_length() - 1)
            st.write(f"Estimated entropy: ~{entropy} bits")
            
            if entropy < 40:
                st.write("❌ Low entropy - could be cracked quickly")
            elif entropy < 60:
                st.write("⚠️ Medium entropy - reasonable protection")
            else:
                st.write("✅ High entropy - strong protection")

if __name__ == "__main__":
    main()
