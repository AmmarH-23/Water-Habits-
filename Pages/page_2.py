import openai
import streamlit as st
import os
import requests
from dotenv import load_dotenv

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load environment variables
load_dotenv()

# Streamlit option menu for navigation
feature = st.selectbox(
    "Choose a Feature",
    ["Sprinkler Control Based on Weather", "Water Conservation Tips"]
)

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

# Function to get weather data
def get_weather_data(city):
    api_key = "06a358e94ea3d909daffbe1a0a009559"  # Replace with your actual API key
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            st.error(f"Error {response.status_code}: Unable to fetch data")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        return None

# Function to decide whether to turn on sprinklers
def control_sprinklers(weather_data):
    if not weather_data:
        return "Unable to determine sprinkler status."

    # Extracting relevant data
    precipitation = weather_data.get('rain', {}).get('1h', 0)  # Precipitation in the last hour (in mm)
    description = weather_data['weather'][0]['description']
    temp = weather_data['main']['temp']

    # Decision logic based on weather conditions
    if precipitation > 0:
        return f"It's raining ({description}), with {precipitation} mm of rain in the last hour. Sprinklers are OFF."
    else:
        return f"No rain detected. Sprinklers are ON to water the garden."

# Function to display "Sprinkler Control Based on Weather" feature
def sprinkler_control_page():
    st.title("Sprinkler Control Based on Weather")

    # Input: City name
    city = st.text_input("Enter the city name", "San Jose")

    # Fetch and display weather data and sprinkler decision
    if st.button("Get Weather & Control Sprinklers"):
        if city:
            weather_data = get_weather_data(city)
            if weather_data:
                # Show weather details
                st.subheader(f"Weather in {city.capitalize()}")
                st.write(f"Description: {weather_data['weather'][0]['description'].capitalize()}")
                st.write(f"Temperature: {weather_data['main']['temp']}°C")
                st.write(f"Humidity: {weather_data['main']['humidity']}%")
                st.write(f"Wind Speed: {weather_data['wind']['speed']} m/s")
                st.write(f"rainfall: {weather_data.get('rain', {}).get('1h', 0)} mm")

                # Get sprinkler decision
                sprinkler_status = control_sprinklers(weather_data)
                st.subheader("Sprinkler Status:")
                st.write(sprinkler_status)
        else:
            st.warning("Please enter a city name.")

# Function to display "Water Conservation Tips" feature
def water_conservation_page():
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

# Function to show content for the page
def show():
    if feature == "Sprinkler Control Based on Weather":
        sprinkler_control_page()  # Display Sprinkler Control page

    elif feature == "Water Conservation Tips":
        water_conservation_page()  # Display Water Conservation Tips page

# Main logic to display the content based on feature selection
show()

