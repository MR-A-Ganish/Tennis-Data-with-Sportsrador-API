import requests
import mysql.connector

def fetch_complexes():
    url = "https://api.sportradar.com/tennis/trial/v3/en/complexes.json?api_key=fLPRPhauH74hYvOVw8CSDONOcPs1Q5esq3jD161p"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

def insert_data(cursor, data):
    for complex_ in data.get('complexes', []):
        complex_id = complex_.get('id')
        complex_name = complex_.get('name')

        cursor.execute("""
            INSERT INTO Complexes (complex_id, complex_name)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE complex_name = %s
        """, (complex_id, complex_name, complex_name))

        for venue in complex_.get('venues', []):
            venue_id = venue.get('id')
            venue_name = venue.get('name')
            city_name = venue.get('city_name', 'N/A')  
            country_name = venue.get('country_name', 'N/A') 
            country_code = venue.get('country_code', 'N/A')
            timezone = venue.get('timezone', 'N/A')

            cursor.execute("""
                INSERT INTO Venues (venue_id, venue_name, city_name, country_name, country_code, timezone, complex_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE venue_name = %s, city_name = %s, country_name = %s, timezone = %s
            """, (venue_id, venue_name, city_name, country_name, country_code, timezone, complex_id,
                venue_name, city_name, country_name, timezone))

def main():
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Ganish*43733001",
        database="tennis_complexes"
    )
    cursor = db.cursor()

    data = fetch_complexes()
    if data:
        insert_data(cursor, data)
        db.commit()

    cursor.close()
    db.close()

if __name__ == "__main__":
    main()
