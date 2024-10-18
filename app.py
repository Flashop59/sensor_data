import streamlit as st
import mysql.connector
import pandas as pd

# Connect to MySQL database
try:
    db = mysql.connector.connect(
        host="mylogger.helioho.st",
        user="omhure_datalogger",
        password="Redmi@6a",  # Replace with your actual password
        database="omhure_datalogger"
    )

    cursor = db.cursor()

    # Fetch data from the table
    cursor.execute("SELECT * FROM sensor_data")  # Adjust the query based on your table structure
    data = cursor.fetchall()

    # Get column names
    columns = [i[0] for i in cursor.description]

    # Convert to pandas DataFrame 
    df = pd.DataFrame(data, columns=columns)

    # Display the data in Streamlit
    st.title("Sensor Data")
    st.dataframe(df)

    # Add a download button for CSV
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='sensor_data.csv',
        mime='text/csv'
    )

    # Close the connection
    cursor.close()
    db.close()

except mysql.connector.Error as err:
    st.error(f"Error: {err}")
