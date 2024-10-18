import streamlit as st
import mysql.connector
import pandas as pd

# Connect to MySQL database
db = mysql.connector.connect(
    host="mylogger.helioho.st",
    user="omhure_datalogger",
    password="Redmi@6a",
    database="omhure_datalogger"
)
cursor = db.cursor()

# Fetch data from the MySQL table
cursor.execute("SELECT timestamp, current, voltage FROM sensor_data")
data = cursor.fetchall()

# Convert to pandas DataFrame
df = pd.DataFrame(data, columns=["timestamp", "current", "voltage"])

# Streamlit app
st.title('Sensor Data Dashboard')

# Display a line chart of current and voltage over time
st.line_chart(df.set_index('timestamp')[["current", "voltage"]])
