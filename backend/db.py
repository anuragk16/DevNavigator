import mysql.connector
import pandas as pd
import json
from sqlalchemy import create_engine

config = {
        "user": "anurag",
        "password": "63789",
        "host": "localhost",
        "database": "devnavigator"
    }

def get_material():
    # Create a connection string for SQLAlchemy
    connection_url = f"mysql+mysqlconnector://{config['user']}:{config['password']}@{config['host']}/{config['database']}"
    
    # Create an SQLAlchemy engine
    engine = create_engine(connection_url)

    # Query the database using Pandas
    query = "SELECT * FROM material;"
    df = pd.read_sql(query, con=engine)  # Pass the engine here

    # Convert the DataFrame to a dictionary
    data_dict = df.to_dict(orient="records")

    return df


def execute_query(query):
    conn = mysql.connector.connect(**config)
    df = pd.read_sql(query, conn)
    conn.close()

    return df
    
    
# df = get_material()
# # a = "\n".join([
# #     f"Topic: {row['TOPIC']}, Sub Topics: {row['SUB TOPICS']}, Time Required: {row['TIME REQUIRED']}, "
# #     f"Link (English): {row['LINK (English)']}, Link (Hindi): {row['LINK (Hindi)']}, "
# #     f"Notes: {row['NOTES']}, Project: {row['PROJECT']}"
# #     for _, row in df.iterrows()
# # ])
# print(df)