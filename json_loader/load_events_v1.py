import json
import os

import psycopg
from psycopg import Error

import psycopg

class PostgreSQLDatabase:
    def __init__(self, user='', password='', host='localhost', port='5432', database='project_database'):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.connection = None

    def connect_to_database(self):
        # Database credentials and address
        url = f"host={self.host} port={self.port} dbname={self.database}"
        
        # If username/password needed add them to the url
        if(self.user != ""):
            url += f" user={self.user}"
        if(self.password != ""):
            url += f" password={self.password}"

        try:
            self.connection = psycopg.connect(url)
            return True
        except Exception as error:
            print(error)
            return False

    def insert_data(self, table_name, data):
        try:
            if not self.connection:
                print("No active connection to the database.")
                return

            cursor = self.connection.cursor()

            # Construct the insert query dynamically based on the number of columns
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

            # Execute the insert query
            cursor.execute(insert_query, list(data.values()))

            # Commit the transaction
            self.connection.commit()
            # print("Record inserted successfully")

        except psycopg.Error as error:
            print("Error while inserting data into PostgreSQL:", error)

    def close_connection(self):
        try:
            # Close database connection
            if self.connection:
                self.connection.close()
                print("PostgreSQL connection is closed")
        except Exception as e:
            print("Error while closing connection:", e)

def write_json_to_db(filePath, db, tableName):
    # Open and load the JSON file
    with open(filePath, 'r') as file:
        data = json.load(file)
    
    for event in data: # Get one of all unique events types

        data_to_insert = {}
        
        # for col in ['id', 'index', 'period', 'timestamp', 'minute', 'second', 'type', 'possession', 'possession_team', 'play_pattern', 'team']:
        #     data_to_insert[col] = event[col]

        data_to_insert = {
            "id": event['id'],
            "index": event['index'],
            "period": event['period'],
            "timestamp": event['timestamp'],
            "minute": event['minute'],
            "second": event['second'],
            "type":  event['type']['id'],
            "possession": event['possession'],
            "possession_team": event['possession_team']['id'],
            "play_pattern": event['play_pattern']['id'],
            "team": event['team']['id'],
        }
        if db:
            db.insert_data(table_name, data_to_insert)

dirPath = "/Users/abdullah/comp_3005_final_project/open-data-0067cae166a56aa80b2ef18f61e16158d6a7359a/data/events/"
files = os.listdir(dirPath)

if __name__ == "__main__":

    db = PostgreSQLDatabase()
    db.connect_to_database()

    table_name = 'events'

    for file in files:
        filePath = os.path.join(dirPath, file)
        
        write_json_to_db(filePath, db, table_name)

    if db:
        db.close_connection(connection)






