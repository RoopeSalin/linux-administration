#!/usr/bin/env python3
import mysql.connector
import os
import pytz
import requests

from datetime import datetime
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
CITY = 'Helsinki'
URL = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric'

conn = mysql.connector.connect(
    host="localhost",
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_USER_PWD"),
    database=os.getenv("DB_NAME")
)

cursor = conn.cursor()
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS weather_data (id INT
    AUTO_INCREMENT PRIMARY KEY, city VARCHAR(50), temperature FLOAT, 
    description VARCHAR(100), timestamp DATETIME)'''
)

response = requests.get(URL)
data = response.json()
temp = data['main']['temp']
desc = data['weather'][0]['description']
timestamp = datetime.now().astimezone(pytz.timezone('Europe/Helsinki'))

cursor.execute('INSERT INTO weather_data (city, temperature, description, timestamp) VALUES (%s, %s, %s, %s)', (CITY, temp, desc, timestamp))
conn.commit()
cursor.close()
conn.close()

print(f'Data tallennettu: {CITY} {temp}°C {desc}')