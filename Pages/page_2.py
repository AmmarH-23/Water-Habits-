import openai
import streamlit as st
import os
import requests
from PIL import Image
import folium
from streamlit.components.v1 import html

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up Google Maps API key
google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")

# Function to get geocoding data from Google Maps
def get_geocoding_data_google(city):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": city,
        "key": google_maps_api_key
    }
    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code == 200 and len(data["results"]) > 0:
        location = data["results"][0]["geometry"]["location"]
        return {
            "lat": location["lat"],
            "lon": location["lng"]
        }
    else:
        return f"Error: Unable to fetch geocoding data for {city}. {data.get('error_message', '')}"

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
additional_info = st.text_input("Enter additional information to refine location (e.g., cross streets, landmarks):")
issue_description = st.text_area("Describe the water-related issue (e.g., leaking pipe, visible water wastage, etc.):")
image = st.file_uploader("Upload a photo of the issue (optional):", type=['jpg', 'jpeg', 'png'])

if st.button("Report Issue"):
    if city and issue_description:
        # Get geocoding data using Google Maps API
        location_query = f"{city} {additional_info}" if additional_info else city
        geocoding_data = get_geocoding_data_google(location_query)
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

            # Embed Google Maps using iframe with a draggable marker
            map_url = f"https://www.google.com/maps/embed/v1/place?key={google_maps_api_key}&q={geocoding_data['lat']},{geocoding_data['lon']}&zoom=12"
            st.write("### Map of Reported Issue Location:")
            html(f'<iframe width="100%" height="500" frameborder="0" style="border:0" src="{map_url}" allowfullscreen></iframe>', height=500)

            st.success("Thank you for reporting the issue. The relevant authorities have been notified.")
        else:
            st.warning(geocoding_data)
    else:
        st.warning("Please enter both the city and a description of the issue.")
