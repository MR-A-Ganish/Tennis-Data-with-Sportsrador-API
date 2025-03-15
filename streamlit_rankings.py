import streamlit as st
import requests

def fetch_rankings():
    url = "https://api.sportradar.com/tennis/trial/v3/en/double_competitors_rankings.json?api_key=fLPRPhauH74hYvOVw8CSDONOcPs1Q5esq3jD161p"
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

def extract_rankings(data):
    rankings_list = data.get("rankings", [])
    
    extracted_data = []
    for ranking in rankings_list:
        year = ranking.get("year", "Unknown")
        week = ranking.get("week", "Unknown")
        gender = ranking.get("gender", "Unknown")
        
        for player in ranking.get("competitor_rankings", []):  
            extracted_data.append({
                "year": year,
                "week": week,
                "gender": gender,
                "rank": player.get("rank", "N/A"),
                "previous_rank": player.get("previous_rank", "N/A"),
                "points": player.get("points", "N/A"),
                "competitor_id": player.get("competitor", {}).get("id", "N/A"),
                "competitor_name": player.get("competitor", {}).get("name", "Unknown Player"),
                "competitor_nationality": player.get("competitor", {}).get("nationality", "N/A")
            })
    
    return extracted_data

st.title("🎾 Double Competitors Rankings Explorer")

data = fetch_rankings()

if data:
    rankings = extract_rankings(data)

    st.sidebar.header("Filters")

    if rankings:
        years = sorted(set(rank["year"] for rank in rankings))
        weeks = sorted(set(rank["week"] for rank in rankings))
        genders = sorted(set(rank["gender"] for rank in rankings))

        selected_year = st.sidebar.selectbox("Select Year", years, index=len(years)-1)
        selected_week = st.sidebar.selectbox("Select Week", weeks, index=len(weeks)-1)
        selected_gender = st.sidebar.selectbox("Select Gender", genders)
        rank_range = st.sidebar.slider("Select Rank Range", min_value=1, max_value=500, value=(1, 50))

        filtered_rankings = [
            rank for rank in rankings
            if rank["year"] == selected_year
            and rank["week"] == selected_week
            and rank["gender"] == selected_gender
            and rank_range[0] <= rank["rank"] <= rank_range[1]
        ]

        st.subheader("Filtered Player Rankings")

        if filtered_rankings:
            for rank in filtered_rankings:
                with st.expander(f"🏆 Rank {rank['rank']} - {rank['competitor_name']}"):
                    st.write(f"**Competitor ID:** {rank['competitor_id']}")
                    st.write(f"**Name:** {rank['competitor_name']}")
                    st.write(f"**Rank:** {rank['rank']}")
                    st.write(f"**Points:** {rank['points']}")
                    st.write(f"**Previous Rank:** {rank['previous_rank']}")
                    st.write(f"**Nationality:** {rank['competitor_nationality']}")
        else:
            st.warning("No players match your selected filters.")
    else:
        st.error("No rankings found in the API response.")
