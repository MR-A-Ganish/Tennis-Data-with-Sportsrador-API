import streamlit as st
import requests

def fetch_competitions():
    url = "https://api.sportradar.com/tennis/trial/v3/en/competitions.json?api_key=fLPRPhauH74hYvOVw8CSDONOcPs1Q5esq3jD161p"
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
def extract_competitions(data):
    return data.get("competitions", []) if data else []

st.title("🎾 Tennis Competitions Explorer")

data = fetch_competitions()

if data:
    competitions = extract_competitions(data)
    
    st.sidebar.header("Filters")
    
    if competitions:
        competition_options = {comp["name"]: comp for comp in competitions}
        selected_competition_name = st.sidebar.selectbox("Select Competition", competition_options.keys())
        selected_competition = competition_options[selected_competition_name]

        selected_type = st.sidebar.selectbox("Select Type", ["All", "singles", "doubles"])

        available_genders = list(set(comp.get("gender", "") for comp in competitions if comp.get("gender", "")))
        available_genders.insert(0, "All")  
        selected_gender = st.sidebar.selectbox("Select Gender", available_genders)

        filtered_competitions = [selected_competition]

        if selected_type != "All":
            filtered_competitions = [comp for comp in filtered_competitions if comp["type"] == selected_type]
        
        if selected_gender != "All":
            filtered_competitions = [comp for comp in filtered_competitions if comp.get("gender", "").lower() == selected_gender.lower()]

        st.subheader(f"Competitions Available")

        if filtered_competitions:
            for comp in filtered_competitions:
                with st.expander(f"🏆 {comp['name']}"):
                    st.write(f"**ID:** {comp['id']}")
                    st.write(f"**Type:** {comp['type']}")
                    st.write(f"**Gender:** {comp.get('gender', 'N/A')}")
                    st.write(f"**Level:** {comp.get('level', 'N/A')}")
                    st.write(f"**Alternative Name:** {comp.get('alternative_name', 'N/A')}")
        else:
            st.warning("No competitions match your filters.")
    else:
        st.error("No competitions found in the API response.")




