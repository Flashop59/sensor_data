import streamlit as st
import mysql.connector
import pandas as pd

# Set the page to refresh every 5 seconds
st.set_page_config(page_title="Sensor Data", layout="wide")

# Add autorefresh (useful in local environments; this will simulate an interval-based refresh)
st_autorefresh = st.empty()
st_autorefresh.empty()

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

# Fetch and display data in a placeholder for refreshing
data_placeholder = st.empty()
df = fetch_data()
if not df.empty:
    data_placeholder.dataframe(df)  # Display the data with the latest entries on top

    # CSV download button
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='sensor_data.csv',
        mime='text/csv'
    )
