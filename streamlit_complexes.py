import streamlit as st
import requests

def fetch_complexes():
    url = "https://api.sportradar.com/tennis/trial/v3/en/complexes.json?api_key=fLPRPhauH74hYvOVw8CSDONOcPs1Q5esq3jD161p"
    headers = {"accept": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code} - {response.reason}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        return None

def extract_complexes(data):
    return data.get("complexes", []) if data else []

st.title("🎾 Tennis Complexes Explorer")

data = fetch_complexes()

if data:
    complexes = extract_complexes(data)

    st.sidebar.header("Select Complexes")

    if complexes:
        complex_ids = [complex_["id"] for complex_ in complexes]
        complex_names = [complex_["name"] for complex_ in complexes]
        selected_ids = st.sidebar.multiselect("Select Complex IDs", complex_ids)
        selected_names = st.sidebar.multiselect("Select Complex Names", complex_names)
        filtered_complexes = complexes

        if selected_ids:
            filtered_complexes = [complex_ for complex_ in filtered_complexes if complex_["id"] in selected_ids]

        if selected_names:
            filtered_complexes = [complex_ for complex_ in filtered_complexes if complex_["name"] in selected_names]
        st.subheader("Filtered Complexes")

        if filtered_complexes:
            for complex_ in filtered_complexes:
                with st.expander(f"🏟️ {complex_['name']} (ID: {complex_['id']})"):
                    st.write(f"**Complex ID:** {complex_['id']}")
                    st.write(f"**Venue Name:** {complex_['name']}")
                    st.write(f"**City Name:** {complex_.get('city', 'N/A')}")
                    st.write(f"**Country Name:** {complex_.get('country', 'N/A')}")
                    st.write(f"**Country Code:** {complex_.get('country_code', 'N/A')}")
                    st.write(f"**Time Zone:** {complex_.get('time_zone', 'N/A')}")
        else:
            st.warning("No complexes match your selected filters.")
    else:
        st.error("No complexes found in the API response.")