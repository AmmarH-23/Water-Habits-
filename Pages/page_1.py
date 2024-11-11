import openai
import streamlit as st
import os

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to analyze household water usage and provide insights
def analyze_water_usage(water_usage_data):
    prompt = (
        f"You are a water usage expert. Based on the following data, provide insights on how the user can save water: \n"
        f"Water Usage Data: {water_usage_data}"
    )
    try:
        # Use OpenAI API to generate insights
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant focused on analyzing water usage and providing conservation insights."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        return response.choices[0]['message']['content'].strip()
    except Exception as e:
        return f"An error occurred: {e}"

# Show function to be called from main.py
def show():
    st.title("Personalized Water Usage Insights")
    
    # Input form to capture water usage data
    water_usage_data = st.text_area("Enter your water usage data", "e.g., 500 gallons per week")
    
    if st.button("Analyze Water Usage"):
        if water_usage_data:
            insights = analyze_water_usage(water_usage_data)
            st.subheader("Insights")
            st.write(insights)
        else:
            st.warning("Please enter your water usage data.")
