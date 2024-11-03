import streamlit as st
import mysql.connector
import pandas as pd
import time

# Function to fetch data from the database
def fetch_data():
    try:
        db = mysql.connector.connect(
            host="mylogger.helioho.st",
            user="omhure_datalogger",
            password="Redmi@6a",  # Replace with your actual password
            database="omhure_datalogger"
        )

        cursor = db.cursor()
        cursor.execute("SELECT * FROM sensor_data ORDER BY id DESC")  # Latest entries first
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

# Display data and download button outside the loop
df = fetch_data()

# Placeholder for data that will be periodically updated
data_placeholder = st.empty()

# CSV download button (static, placed outside the refresh loop)
if not df.empty:
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='sensor_data.csv',
        mime='text/csv'
    )

# Update the data display every 5 seconds
while True:
    df = fetch_data()
    if not df.empty:
        data_placeholder.dataframe(df)  # Only update the dataframe display

    # Wait for 5 seconds before refreshing
    time.sleep(5)
    st.experimental_rerun()
