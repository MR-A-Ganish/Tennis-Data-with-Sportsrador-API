import requests
import mysql.connector
from mysql.connector import Error
import time

# Define your API URL and MySQL connection details
url = "https://api.sportradar.com/tennis/trial/v3/en/double_competitors_rankings.json?api_key=fLPRPhauH74hYvOVw8CSDONOcPs1Q5esq3jD161p"
headers = {"accept": "application/json"}

# Function to handle retries on failed API request (403 error)
def fetch_data_with_retries(url, headers, retries=3, delay=5):
    for attempt in range(retries):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()  # Return the JSON response if successful
        else:
            print(f"API request failed with status code {response.status_code}. Retrying...")
            time.sleep(delay)  # Wait before retrying
    return None  # Return None if all retries fail

# Fetch Data from the API with retry logic
data = fetch_data_with_retries(url, headers)

if data is not None:
    # Database connection
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            database='tennis_rank',
            user='root',
            password='Ganish*43733001'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Iterate over the rankings
            for ranking in data['rankings']:
                for competitor_ranking in ranking['competitor_rankings']:
                    # Extract competitor details (use .get() to avoid KeyError)
                    competitor = competitor_ranking['competitor']
                    competitor_id = competitor.get('id')
                    name = competitor.get('name')
                    country = competitor.get('country')
                    country_code = competitor.get('country_code', 'N/A')  # Default to 'N/A' if missing
                    abbreviation = competitor.get('abbreviation')

                    # Insert competitor data into Competitors table
                    insert_competitor_query = """
                    INSERT IGNORE INTO Competitors (competitor_id, name, country, country_code, abbreviation)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_competitor_query, (competitor_id, name, country, country_code, abbreviation))
                    
                    # Extract ranking data
                    rank = competitor_ranking.get('rank')
                    movement = competitor_ranking.get('movement')
                    points = competitor_ranking.get('points')
                    competitions_played = competitor_ranking.get('competitions_played')

                    # Insert ranking data into Competitor_Rankings table
                    insert_ranking_query = """
                    INSERT INTO Competitor_Rankings (`rank`, movement, points, competitions_played, competitor_id)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_ranking_query, (rank, movement, points, competitions_played, competitor_id))

            # Commit the transactions to the database
            connection.commit()

            print("Data inserted successfully")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
else:
    print("API request failed after multiple attempts.")
