import requests
import mysql.connector

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Ganish*43733001",
    database="tennis_competitions"
)
cursor = db.cursor()

api_url = "https://api.sportradar.com/tennis/trial/v3/en/competitions.json?api_key=fLPRPhauH74hYvOVw8CSDONOcPs1Q5esq3jD161p"
response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()
    competitions = data.get("competitions", [])

    category_map = {}  
    for comp in competitions:
        category_id = comp["category"]["id"]
        category_name = comp["category"]["name"]

        if category_id not in category_map:
            cursor.execute("SELECT COUNT(*) FROM Categories WHERE category_id = %s", (category_id,))
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO Categories (category_id, category_name) VALUES (%s, %s)", 
                (category_id, category_name))
                category_map[category_id] = category_name  

    for comp in competitions:
        competition_id = comp["id"]
        competition_name = comp["name"]
        parent_id = comp.get("parent_id") 
        competition_type = comp["type"]
        gender = comp["gender"]
        category_id = comp["category"]["id"]

        cursor.execute("SELECT COUNT(*) FROM Competitions WHERE competition_id = %s", (competition_id,))
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO Competitions (competition_id, competition_name, parent_id, type, gender, category_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (competition_id, competition_name, parent_id, competition_type, gender, category_id))

    db.commit()
    print("Data successfully inserted into the database.")

else:
    print(f"Failed to fetch data: {response.status_code}")


cursor.close()
db.close()

