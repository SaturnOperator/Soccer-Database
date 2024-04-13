# Created by Gabriel Martell

'''
Version 1.11 (04/02/2024)
=========================================================
queries.py (Carleton University COMP3005 - Database Management Student Template Code)

This is the template code for the COMP3005 Database Project 1, and must be accomplished on an Ubuntu Linux environment.
Your task is to ONLY write your SQL queries within the prompted space within each Q_# method (where # is the question number).

You may modify code in terms of testing purposes (commenting out a Qn method), however, any alterations to the code, such as modifying the time, 
will be flagged for suspicion of cheating - and thus will be reviewed by the staff and, if need be, the Dean. 

To review the Integrity Violation Attributes of Carleton University, please view https://carleton.ca/registrar/academic-integrity/ 

=========================================================
'''

# Imports
import psycopg
import csv
import subprocess
import os
import re

# Connection Information
''' 
The following is the connection information for this project. These settings are used to connect this file to the autograder.
You must NOT change these settings - by default, db_host, db_port and db_username are as follows when first installing and utilizing psql.
For the user "postgres", you must MANUALLY set the password to 1234.
'''
# root_database_name = "project_database"
# query_database_name = "query_database"
# db_username = 'postgres'
# db_password = '1234'
# db_host = 'localhost'
# db_port = '5432'

root_database_name = "project_database"
query_database_name = "query_database"
db_username = ''
db_password = ''
db_host = 'localhost'
db_port = '5432'

# Directory Path - Do NOT Modify
dir_path = os.path.dirname(os.path.realpath(__file__))

# Loading the Database after Drop - Do NOT Modify
#================================================
def load_database(cursor, conn):
    drop_database(cursor, conn)

    # Create the Database if it DNE
    try:
        conn.autocommit = True
        cursor.execute(f"CREATE DATABASE {query_database_name};")
        conn.commit()
    except Exception as error:
        print(error)
    finally:
        conn.autocommit = False
    conn.close()
    
    # Connect to this query database.
    dbname = query_database_name
    user = db_username
    password = db_password
    host = db_host
    port = db_port
    conn = psycopg.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    return conn  ## @@@@@@@@@@@ DELETE THIS LINE
    
    # Import the dbexport.sql database data into this database
    try:
        command = f'psql -h {host} -U {user} -d {query_database_name} -a -f {os.path.join(dir_path, "dbexport.sql")}'
        env = {'PGPASSWORD': password}
        subprocess.run(command, shell=True, check=True, env=env)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while loading the database: {e}")
    
    # Return this connection.
    return conn    

# Dropping the Database after Query n Execution - Do NOT Modify
#================================================
def drop_database(cursor, conn):
    print("NOT DROPPING TABLE - DELETE THIS EDIT")
    return ## @@@@@@@@ DELETE THIS LINE
    # Drop database if it exists.
    try:
        conn.autocommit = True
        cursor.execute(f"DROP DATABASE IF EXISTS {query_database_name};")
        conn.commit()
    except Exception as error:
        print(error)
        pass
    finally:
        conn.autocommit = False

# Reconnect to Root Database - Do NOT Modify
#================================================
def reconnect(cursor, conn):
    cursor.close()
    conn.close()

    dbname = root_database_name
    user = db_username
    password = db_password
    host = db_host
    port = db_port
    return psycopg.connect(dbname=dbname, user=user, password=password, host=host, port=port)

# Getting the execution time of the query through EXPLAIN ANALYZE - Do NOT Modify
#================================================
def get_time(cursor, conn, sql_query):
    # Prefix your query with EXPLAIN ANALYZE
    explain_query = f"EXPLAIN ANALYZE {sql_query}"

    try:
        # Execute the EXPLAIN ANALYZE query
        cursor.execute(explain_query)
        
        # Fetch all rows from the cursor
        explain_output = cursor.fetchall()
        
        # Convert the output tuples to a single string
        explain_text = "\n".join([row[0] for row in explain_output])
        
        # Use regular expression to find the execution time
        # Look for the pattern "Execution Time: <time> ms"
        match = re.search(r"Execution Time: ([\d.]+) ms", explain_text)
        if match:
            execution_time = float(match.group(1))
            return f"Execution Time: {execution_time} ms"
        else:
            print("Execution Time not found in EXPLAIN ANALYZE output.")
            return f"NA"
    except:
        print("[ERROR] Error getting time.")


# Write the results into some Q_n CSV. If the is an error with the query, it is a INC result - Do NOT Modify
#================================================
def write_csv(execution_time, cursor, conn, i):
    # Collect all data into this csv, if there is an error from the query execution, the resulting time is INC.
    try:
        colnames = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        filename = f"{dir_path}/Q_{i}.csv"

        with open(filename, 'w', encoding='utf-8', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            
            # Write column names to the CSV file
            csvwriter.writerow(colnames)
            
            # Write data rows to the CSV file
            csvwriter.writerows(rows)

    except Exception as error:
        execution_time[i-1] = "INC"
        print(error)
    
#================================================
        
'''
The following 10 methods, (Q_n(), where 1 < n < 10) will be where you are tasked to input your queries.
To reiterate, any modification outside of the query line will be flagged, and then marked as potential cheating.
Once you run this script, these 10 methods will run and print the times in order from top to bottom, Q1 to Q10 in the terminal window.
'''
def Q_1(cursor, conn, execution_time):
    connection = load_database(cursor, conn)
    cursor = connection.cursor()

    #==========================================================================
    # Enter QUERY within the quotes:

    query = """
SELECT p.player_name, AVG(e16.xg_score) AS avg_xg_score
FROM player p
JOIN event_16 e16 ON p.player_id = e16.player_id
-- WHERE e16.season_id = 90
WHERE e16.match_id IN (3764440, 3764661, 3773369, 3773372, 3773377, 3773386, 3773387, 3773403, 3773415, 3773428, 3773457, 3773466, 3773474, 3773477, 3773497, 3773523, 3773526, 3773547, 3773552, 3773565, 3773571, 3773585, 3773586, 3773587, 3773593, 3773597, 3773625, 3773631, 3773656, 3773660, 3773661, 3773665, 3773672, 3773689, 3773695)
GROUP BY p.player_name
ORDER BY avg_xg_score DESC;"""

    #==========================================================================

    time_val = get_time(cursor, connection, query)
    cursor.execute(query)
    execution_time[0] = (time_val)

    write_csv(execution_time, cursor, connection, 1)
    return reconnect(cursor, connection)

def Q_2(cursor, conn, execution_time):

    connection = load_database(cursor, conn)
    cursor = connection.cursor()

    #==========================================================================    
    # Enter QUERY within the quotes:

    query = """
SELECT p.player_name, COUNT(e16.event_id) AS shots_count
FROM player p
JOIN event_16 e16 ON p.player_id = e16.player_id
-- WHERE e16.season_id = 90
WHERE e16.match_id IN (3764440, 3764661, 3773369, 3773372, 3773377, 3773386, 3773387, 3773403, 3773415, 3773428, 3773457, 3773466, 3773474, 3773477, 3773497, 3773523, 3773526, 3773547, 3773552, 3773565, 3773571, 3773585, 3773586, 3773587, 3773593, 3773597, 3773625, 3773631, 3773656, 3773660, 3773661, 3773665, 3773672, 3773689, 3773695)
GROUP BY p.player_name
ORDER BY shots_count DESC;"""

    #==========================================================================

    time_val = get_time(cursor, connection, query)
    cursor.execute(query)
    execution_time[1] = (time_val)

    write_csv(execution_time, cursor, connection, 2)
    return reconnect(cursor, connection)
    
def Q_3(cursor, conn, execution_time):

    connection = load_database(cursor, conn)
    cursor = connection.cursor()

    #==========================================================================    
    # Enter QUERY within the quotes:
    
    query = """
SELECT p.player_name, COUNT(e16.event_id) AS first_time_shots
FROM player p
JOIN event_16 e16 ON p.player_id = e16.player_id
-- WHERE e16.season_id IN (4, 42, 90)
WHERE e16.match_id IN (15946, 15956, 15973, 15978, 15986, 15998, 16010, 16023, 16029, 16056, 16073, 16079, 16086, 16095, 16109, 16120, 16131, 16136, 16149, 16157, 16173, 16182, 16190, 16196, 16205, 16215, 16231, 16240, 16248, 16265, 16275, 16289, 16306, 16317, 303377, 303400, 303421, 303430, 303451, 303470, 303473, 303479, 303487, 303493, 303504, 303516, 303517, 303524, 303532, 303548, 303596, 303600, 303610, 303615, 303634, 303652, 303664, 303666, 303674, 303680, 303682, 303696, 303700, 303707, 303715, 303725, 303731, 3764440, 3764661, 3773372, 3773377, 3773386, 3773387, 3773403, 3773415, 3773428, 3773457, 3773466, 3773474, 3773477, 3773497, 3773523, 3773526, 3773547, 3773552, 3773565, 3773571, 3773585, 3773586, 3773587, 3773593, 3773597, 3773625, 3773631, 3773656, 3773660, 3773661, 3773665, 3773672, 3773689, 3773695)
AND e16.first_time = TRUE
GROUP BY p.player_name
ORDER BY first_time_shots  DESC;"""

    #==========================================================================

    time_val = get_time(cursor, connection, query)
    cursor.execute(query)
    execution_time[2] = (time_val)

    write_csv(execution_time, cursor, connection, 3)
    return reconnect(cursor, connection)

def Q_4(cursor, conn, execution_time):
    connection = load_database(cursor, conn)
    cursor = connection.cursor()

    #==========================================================================    
    # Enter QUERY within the quotes:
    
    query = """
SELECT t.team_name, COUNT(e30.event_id) AS passes_count
FROM team t
JOIN event_30 e30 ON t.team_id = e30.team_id
-- WHERE e30.season_id = 90
WHERE e30.match_id IN (3764440, 3764661, 3773369, 3773372, 3773377, 3773386, 3773387, 3773403, 3773415, 3773428, 3773457, 3773466, 3773474, 3773477, 3773497, 3773523, 3773526, 3773547, 3773552, 3773565, 3773571, 3773585, 3773586, 3773587, 3773593, 3773597, 3773625, 3773631, 3773656, 3773660, 3773661, 3773665, 3773672, 3773689, 3773695)
GROUP BY t.team_name
ORDER BY passes_count DESC;"""

    #==========================================================================

    time_val = get_time(cursor, connection, query)
    cursor.execute(query)
    execution_time[3] = (time_val)

    write_csv(execution_time, cursor, connection, 4)
    return reconnect(cursor, connection)

def Q_5(cursor, conn, execution_time):
    connection = load_database(cursor, conn)
    cursor = connection.cursor()

    #==========================================================================    
    # Enter QUERY within the quotes:
    
    query = """
SELECT p.player_name, COUNT(e30.recipient_id) AS recipient_count
FROM player p
JOIN event_30 e30 ON p.player_id = e30.recipient_id
-- WHERE e30.season_id = 44
WHERE e30.match_id IN (3749052, 3749068, 3749079, 3749108, 3749117, 3749133, 3749153, 3749192, 3749196, 3749233, 3749246, 3749253, 3749257, 3749274, 3749276, 3749278, 3749296, 3749310, 3749346, 3749358, 3749360, 3749403, 3749431, 3749434, 3749448, 3749453, 3749454, 3749462, 3749465, 3749493, 3749522, 3749526, 3749528, 3749552, 3749590, 3749603, 3749631, 3749642)
GROUP BY p.player_name
ORDER BY recipient_count DESC;"""

    #==========================================================================

    time_val = get_time(cursor, connection, query)
    cursor.execute(query)
    execution_time[4] = (time_val)

    write_csv(execution_time, cursor, connection, 5)
    return reconnect(cursor, connection)

def Q_6(cursor, conn, execution_time):
    connection = load_database(cursor, conn)
    cursor = connection.cursor()

    #==========================================================================    
    # Enter QUERY within the quotes:
    
    query = """
SELECT t.team_name, COUNT(e16.event_id) AS shots_count
FROM team t
JOIN event_16 e16 ON t.team_id = e16.team_id
-- WHERE e16.season_id = 44
WHERE e16.match_id IN (3749052, 3749068, 3749079, 3749108, 3749117, 3749133, 3749153, 3749192, 3749196, 3749233, 3749246, 3749253, 3749257, 3749274, 3749276, 3749278, 3749296, 3749310, 3749346, 3749358, 3749360, 3749403, 3749431, 3749434, 3749448, 3749453, 3749454, 3749462, 3749465, 3749493, 3749522, 3749526, 3749528, 3749552, 3749590, 3749603, 3749631, 3749642)
GROUP BY t.team_name
ORDER BY shots_count DESC;"""

    #==========================================================================

    time_val = get_time(cursor, connection, query)
    cursor.execute(query)
    execution_time[5] = (time_val)

    write_csv(execution_time, cursor, connection, 6)
    return reconnect(cursor, connection)

def Q_7(cursor, conn, execution_time):
    connection = load_database(cursor, conn)
    cursor = connection.cursor()

    #==========================================================================    
    # Enter QUERY within the quotes:
    
    query = """
SELECT p.player_name, COUNT(e30.event_id) AS through_balls_count
FROM event_30 e30
JOIN player p ON e30.player_id = p.player_id 
-- WHERE e30.season_id = 90
WHERE e30.match_id IN (3764440, 3764661, 3773369, 3773372, 3773377, 3773386, 3773387, 3773403, 3773428, 3773457, 3773466, 3773474, 3773477, 3773497, 3773523, 3773526, 3773547, 3773552, 3773565, 3773571, 3773585, 3773586, 3773587, 3773593, 3773597, 3773625, 3773631, 3773656, 3773660, 3773661, 3773665, 3773672, 3773689, 3773695) 
AND e30.through_ball = True
GROUP BY p.player_name
ORDER BY through_balls_count DESC;"""

    #==========================================================================

    time_val = get_time(cursor, connection, query)
    cursor.execute(query)
    execution_time[6] = (time_val)

    write_csv(execution_time, cursor, connection, 7)
    return reconnect(cursor, connection)

def Q_8(cursor, conn, execution_time):
    connection = load_database(cursor, conn)
    cursor = connection.cursor()

    #==========================================================================    
    # Enter QUERY within the quotes:
    
    query = """
SELECT t.team_name, COUNT(e30.event_id) AS through_balls_count
FROM event_30 e30
JOIN team t ON e30.team_id = t.team_id
-- WHERE e30.season_id = 90
WHERE e30.match_id IN (3764440, 3764661, 3773369, 3773372, 3773377, 3773386, 3773387, 3773403, 3773428, 3773457, 3773466, 3773474, 3773477, 3773497, 3773523, 3773526, 3773547, 3773552, 3773565, 3773571, 3773585, 3773586, 3773587, 3773593, 3773597, 3773625, 3773631, 3773656, 3773660, 3773661, 3773665, 3773672, 3773689, 3773695)
AND e30.through_ball = True
GROUP BY t.team_name
ORDER BY through_balls_count DESC;"""

    #==========================================================================

    time_val = get_time(cursor, connection, query)
    cursor.execute(query)
    execution_time[7] = (time_val)

    write_csv(execution_time, cursor, connection, 8)
    return reconnect(cursor, connection)

def Q_9(cursor, conn, execution_time):
    connection = load_database(cursor, conn)
    cursor = connection.cursor()

    #==========================================================================    
    # Enter QUERY within the quotes:
    
    query = """
SELECT p.player_name, COUNT(e14.event_id) AS completed_dribbles
FROM player p
JOIN event_14 e14 ON p.player_id = e14.player_id
-- WHERE e14.season_id IN (4, 42, 90)
WHERE e14.match_id IN (15946, 15956, 15973, 15978, 15986, 15998, 16010, 16023, 16029, 16056, 16073, 16079, 16086, 16095, 16109, 16120, 16131, 16136, 16149, 16157, 16173, 16182, 16190, 16196, 16205, 16215, 16231, 16240, 16248, 16265, 16275, 16289, 16306, 16317, 303377, 303400, 303421, 303430, 303451, 303470, 303473, 303479, 303487, 303493, 303504, 303516, 303517, 303524, 303532, 303548, 303596, 303600, 303610, 303615, 303634, 303652, 303664, 303666, 303674, 303680, 303682, 303696, 303700, 303707, 303715, 303725, 303731, 3764440, 3764661, 3773369, 3773372, 3773377, 3773386, 3773387, 3773403, 3773415, 3773428, 3773457, 3773466, 3773474, 3773477, 3773497, 3773523, 3773526, 3773547, 3773552, 3773565, 3773571, 3773585, 3773586, 3773587, 3773593, 3773597, 3773625, 3773631, 3773656, 3773660, 3773661, 3773665, 3773672, 3773689, 3773695)
AND e14.complete = TRUE
GROUP BY p.player_name
ORDER BY completed_dribbles DESC;"""

    #==========================================================================

    time_val = get_time(cursor, connection, query)
    cursor.execute(query)
    execution_time[8] = (time_val)

    write_csv(execution_time, cursor, connection, 9)
    return reconnect(cursor, connection)

def Q_10(cursor, conn, execution_time):
    connection = load_database(cursor, conn)
    cursor = connection.cursor()

    #==========================================================================    
    # Enter QUERY within the quotes:
    
    query = """
SELECT p.player_name, COUNT(e39.event_id) AS dribbled_past
FROM player p
JOIN event_39 e39 ON p.player_id = e39.player_id
-- WHERE e39.season_id = 90
WHERE e39.match_id IN (3764440, 3764661, 3773369, 3773372, 3773377, 3773386, 3773387, 3773403, 3773415, 3773428, 3773457, 3773466, 3773474, 3773477, 3773497, 3773523, 3773526, 3773547, 3773552, 3773565, 3773571, 3773585, 3773586, 3773587, 3773593, 3773597, 3773625, 3773631, 3773656, 3773660, 3773661, 3773665, 3773672, 3773689, 3773695)
GROUP BY p.player_name
ORDER BY dribbled_past ASC;"""

    #==========================================================================

    time_val = get_time(cursor, connection, query)
    cursor.execute(query)
    execution_time[9] = (time_val)

    write_csv(execution_time, cursor, connection, 10)
    return reconnect(cursor, connection)

# Running the queries from the Q_n methods - Do NOT Modify
#=====================================================
def run_queries(cursor, conn, dbname):

    execution_time = [0,0,0,0,0,0,0,0,0,0]

    conn = Q_1(cursor, conn, execution_time)
    conn = Q_2(cursor, conn, execution_time)
    conn = Q_3(cursor, conn, execution_time)
    conn = Q_4(cursor, conn, execution_time)
    conn = Q_5(cursor, conn, execution_time)
    conn = Q_6(cursor, conn, execution_time)
    conn = Q_7(cursor, conn, execution_time)
    conn = Q_8(cursor, conn, execution_time)
    conn = Q_9(cursor, conn, execution_time)
    conn = Q_10(cursor, conn, execution_time)

    for i in range(10):
        print(execution_time[i])

    print("SUM:", sum([float(ms.split(":")[1].split(" ms")[0]) for ms in execution_time]))

''' MAIN '''
try:
    if __name__ == "__main__":

        dbname = root_database_name
        user = db_username
        password = db_password
        host = db_host
        port = db_port

        conn = psycopg.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        cursor = conn.cursor()
        
        run_queries(cursor, conn, dbname)
except Exception as error:
    print(error)
    #print("[ERROR]: Failure to connect to database.")
#_______________________________________________________
