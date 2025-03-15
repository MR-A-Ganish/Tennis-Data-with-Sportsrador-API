import requests
import mysql.connector

API_URL = "https://api.sportradar.com/tennis/trial/v3/en/double_competitors_rankings.json"
API_KEY = "fLPRPhauH74hYvOVw8CSDONOcPs1Q5esq3jD161p"

def fetch_rankings():
    """Fetch data from the API"""
    response = requests.get(f"{API_URL}?api_key={API_KEY}")

    if response.status_code == 200:
        return response.json()  
    else:
        print(f"Error fetching data: {response.status_code}")
        print("Response:", response.text)
        return None  

def insert_data(cursor, data):
    """Insert data into MySQL database"""
    for ranking in data.get('rankings', []):  
        for competitor in ranking.get('competitors', []): 

            
            competitor_id = competitor.get('id')
            name = competitor.get('name')
            country = competitor.get('country', 'N/A')
            country_code = competitor.get('country_code', 'N/A')
            abbreviation = competitor.get('abbreviation', 'N/A')

            
            cursor.execute("""
                INSERT INTO Competitors (competitor_id, name, country, country_code, abbreviation)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE name=%s, country=%s, country_code=%s, abbreviation=%s
            """, (competitor_id, name, country, country_code, abbreviation, name, country, country_code, abbreviation))

            
            rank = competitor.get('rank')
            movement = competitor.get('movement', 0)
            points = competitor.get('points', 0)
            competitions_played = competitor.get('competitions_played', 0)

            
            cursor.execute("""
                INSERT INTO Competitor_Rankings (`rank`, movement, points, competitions_played, competitor_id)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE `rank`=%s, movement=%s, points=%s, competitions_played=%s
            """, (rank, movement, points, competitions_played, competitor_id, rank, movement, points, competitions_played))

def main():
    """Main function to connect to the database and insert data"""
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Ganish*43733001", 
        database="TENNIS_RANKING"
    )
    cursor = db.cursor()

    
    data = fetch_rankings()
    
    if data:
        insert_data(cursor, data)
        db.commit()  

    cursor.close()
    db.close()
    print("✅ Data inserted successfully!")

if __name__ == "__main__":
    main()
data = fetch_rankings()
print(data) 
