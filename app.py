import streamlit as st
import mysql.connector
import pandas as pd
import time

# Refresh every 5 seconds
st.experimental_set_query_params(placeholder="refresh")
st.set_page_config(page_title="Sensor Data", layout="wide", initial_sidebar_state="collapsed")

# Define a function to fetch data from the database
def fetch_data():
    try:
        db = mysql.connector.connect(
            host="mylogger.helioho.st",
            user="omhure_datalogger",
            password="Redmi@6a",  # Replace with your actual password
            database="omhure_datalogger"
        )

        cursor = db.cursor()
        cursor.execute("SELECT * FROM sensor_data ORDER BY id DESC")  # Adjust to sort by newest entry
        data = cursor.fetchall()
        columns = [i[0] for i in cursor.description]
        cursor.close()
        db.close()
        return pd.DataFrame(data, columns=columns)

    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return pd.DataFrame()

# Main section of the Streamlit app
st.title("Sensor Data")

while True:
    df = fetch_data()
    if not df.empty:
        st.dataframe(df)  # Display the data with latest entries on top

        # CSV download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='sensor_data.csv',
            mime='text/csv'
        )
    
    # Refresh every 5 seconds
    time.sleep(5)
    st.experimental_rerun()
