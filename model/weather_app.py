import streamlit as st

st.title("Your Personal Weather Assitant")
city = st.text_input("Please type in the city name")
if city:
    st.write(f"Checking the weather for {city}...")