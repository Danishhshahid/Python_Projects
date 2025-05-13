import streamlit as st
import pandas as pd



st.title("BMI calculator")

height = st.slider("Enter your height in cm",100,250,175)
weight = st.slider("Enter your weight in kg",40,100,50)

if st.button("Calculate BMI"):
    bmi = weight / ((height/100)**2)
    st.write(f"Your BMI is {bmi:.2f}")

st.write("### BMI categories ###")
st.write("- Underweight : BMI less than 18.5 ")
st.write("- Normal weight: BMI between 18.5 and 24.5")
st.write("- Over weight: BMI between 24.5 and 29.5")
st.write("- Obesity: BMI 30 or greater")

