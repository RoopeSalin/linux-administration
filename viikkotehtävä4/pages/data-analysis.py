import mysql.connector
import os
import pandas as pd
import plotly.express as px
import streamlit as st

from dotenv import load_dotenv

def main():
    load_dotenv(dotenv_path="../.env")
    conn = mysql.connector.connect(
        host="localhost",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_USER_PWD"),
        database=os.getenv("DB_NAME")
    )

    st.set_page_config(
        page_title = "Säädataa Helsingistä"
    )

    df = pd.read_sql('SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 50', conn)
    
    st.title("Lämpötila Helsingissä") 
    ff = px.line(df, x='timestamp', y='temperature')
    st.plotly_chart(ff, use_container_width=True)
    
    conn.close()
    st.title('Säädata Helsingistä')
    st.dataframe(df)


if __name__ == "__main__":
    main()