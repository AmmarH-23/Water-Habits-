# Water-Habits-

import streamlit as st
from streamlit_option_menu import option_menu
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Custom CSS to set the background image
page_bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
    background-color: #87CEEB;  /* Light blue color */
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Display logo at the top of the sidebar
st.sidebar.image("/Users/dapensilver/Water-Habits-/water-habits/.streamlit/water .webp", use_column_width = True )  # Adjust path and width


# Sidebar menu for navigation
from streamlit_option_menu import option_menu

# Sidebar navigation menu
feature = option_menu(
    "Menu",
    ["Personalized Water Usage Insights", "Sprinkler Control Based on Weather", "Smart Irrigation Recommendations"],
    icons=["droplet", "cloud-sun", "water"],
    menu_icon="cast",
    default_index=0,
    styles={
        "container": {"background-color": "#F0F2F6"},
        "icon": {"color": "#4B9CD3", "font-size": "20px"},
        "nav-link": {"font-size": "18px", "text-align": "left", "margin": "5px"},
        "nav-link-selected": {"background-color": "#4B9CD3"},
    }
)
sidebar_title = '''
<style>
.sidebar-title {
    font-size: 30px;
    font-weight: bold;
}
</style>
'''
st.sidebar.markdown(sidebar_title, unsafe_allow_html=True)
st.sidebar.markdown('<p class="sidebar-title">Water Habits</p>', unsafe_allow_html=True)

 #Display the selected feature
if feature == "Personalized Water Usage Insights":
    st.sidebar.subheader("Personalized Water Usage Insights")
    
elif feature == "Sprinkler Control Based on Weather":
    st.sidebar.subheader("Sprinkler Control Based on Weather")
    

elif feature == "Smart Irrigation Recommendations":
    st.sidebar.subheader("Smart Irrigation Recommendations")
   

# Display content based on feature selection
if feature == "Personalized Water Usage Insights":
    import page_1
    st.write("Loading Personalized Water Usage Insights...")
    page_1.show()

elif feature == "Sprinkler Control Based on Weather":
    import page_2
    st.write("Loading Sprinkler Control Based on Weather...")
    page_2.show()

elif feature == "Smart Irrigation Recommendations":
    import page_3
    st.write("Loading Smart Irrigation Recommendations...")
    page_3.show()
import streamlit as st

st.markdown(
    """
    <style>
    .stApp {
        background-image: url("/Users/dapensilver/Water-Habits-/water-habits/.streamlit/water .webp");
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)
