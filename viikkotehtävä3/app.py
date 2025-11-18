from dotenv import load_dotenv

import mysql.connector
import os
import pandas as pd
import plotly.express as px
import streamlit as st

def main():
    load_dotenv(dotenv_path="../.env")
    conn = mysql.connector.connect(
        host="localhost",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_USER_PWD"),
        database=os.getenv("DB_NAME")
    )

    st.title("Number of monthly passengers on transatlantic flights, 1958-1960") 
    df = pd.read_sql("SELECT * FROM airtravel", conn)
    df = df.rename(columns={"year_1958": "1958","year_1959":"1959","year_1960":"1960"})
    ff = px.line(df, x='Month', y=['1958', '1959', '1960'])
    ff.update_yaxes(title_text="Number of Passengers")
    st.plotly_chart(ff, use_container_width=True)

if __name__ == "__main__":
    main()