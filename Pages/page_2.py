import openai
import streamlit as st
import os
import requests
from PIL import Image

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up OpenWeatherMap API key
openweathermap_api_key = os.getenv("OPENWEATHERMAP_API_KEY")

# Function to get geocoding data from OpenWeatherMap
def get_geocoding_data(city):
    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": city,
        "appid": openweathermap_api_key
    }
    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code == 200 and len(data) > 0:
        return {
            "lat": data[0]["lat"],
            "lon": data[0]["lon"]
        }
    else:
        return f"Error: Unable to fetch geocoding data for {city}. {data.get('message', '')}"

# Function to categorize reported issues using OpenAI
def categorize_issue(description):
    prompt = f"You are an assistant that categorizes community-reported water issues. Please categorize the following issue: {description}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50
        )
        return response.choices[0]['message']['content'].strip()
    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit UI setup
st.title("Community Water Conservation Reporting Tool")

# User inputs for reporting an issue
city = st.text_input("Enter the city where the issue is located:")
issue_description = st.text_area("Describe the water-related issue (e.g., leaking pipe, visible water wastage, etc.):")
image = st.file_uploader("Upload a photo of the issue (optional):", type=['jpg', 'jpeg', 'png'])

if st.button("Report Issue"):
    if city and issue_description:
        # Get geocoding data
        geocoding_data = get_geocoding_data(city)
        if isinstance(geocoding_data, dict):
            st.write(f"### Location Coordinates for {city}")
            st.write(f"Latitude: {geocoding_data['lat']}, Longitude: {geocoding_data['lon']}")

            # Categorize the issue using OpenAI
            category = categorize_issue(issue_description)
            st.write("### Issue Category:")
            st.write(category)

            # Display uploaded image if available
            if image is not None:
                img = Image.open(image)
                st.image(img, caption='Uploaded Image', use_column_width=True)

            st.success("Thank you for reporting the issue. The relevant authorities have been notified.")
        else:
            st.warning(geocoding_data)
    else:
        st.warning("Please enter both the city and a description of the issue.")
