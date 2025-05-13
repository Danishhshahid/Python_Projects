import random
import streamlit as st



# print("Wellcome to Password Generator")

# chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*().,?0123456789'

# number = int(input("enter the amount to passwords to generate: "))
# # number = int(number)
# length = int(input("Enter the required length of password: "))
# # length = int(length)

# print("\n Here are your Passwords: ")

# for pwd in range(number):
#     passwords = ''
#     for c in range(length):
#         passwords += random.choice(chars)
#     print(passwords)


#Render on streamlit

st.title("Wellcome to Password Generator")

chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*().,?0123456789'

number = st.number_input("enter the amount to passwords to generate: ",min_value=1,step=1)
# number = int(number)
length = st.number_input("Enter the required length of password: ",min_value=1,step=1)
# length = int(length)

if st.button("Generate Passwords !"):
    st.subheader("Here are your Generated Passwords")
    for pwd in range(number):
        passwords = ''
        for c in range(length):
            passwords += random.choice(chars)
        st.code(passwords)

    