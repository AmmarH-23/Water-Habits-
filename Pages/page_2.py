import openai
import streamlit as st
import os

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to get water conservation tips from OpenAI
def get_water_conservation_tips(user_input):
    prompt = f"You are a water conservation expert. Provide personalized water-saving tips for the following scenario: {user_input}"
    try:
        # Use the OpenAI API to get the response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant focused on water conservation."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        return response.choices[0]['message']['content'].strip()
    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit UI setup
st.title("Water Conservation Tips Chatbot")

# User inputs for personalized water conservation tips
user_input = st.text_area("Describe your water usage habits or any specific questions you have about saving water:")

if st.button("Get Water Conservation Tips"):
    if user_input:
        # Get conservation tips from OpenAI
        conservation_tips = get_water_conservation_tips(user_input)
        st.write("### Personalized Water Conservation Tips:")
        st.write(conservation_tips)
    else:
        st.warning("Please enter a description of your water usage habits to get tips.")
