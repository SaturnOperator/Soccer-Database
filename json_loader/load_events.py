import json
import os

import psycopg
from psycopg import Error

DATA_DIR = "/Users/abdullah/comp_3005_final_project/open-data-0067cae166a56aa80b2ef18f61e16158d6a7359a/data/"

def get_json_data(file_name):
    file_path = os.path.join(DATA_DIR, file_name)
    with open(file_path, 'r') as file:
        data = json.load(file)

    return data

class PostgresDatabase:
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

# Step 1: Get Competitions data by cometition name and season
def get_competitions_data(filter_list):
    data = get_json_data("competitions.json")

    competitions = []

    # Find matching competitions from competitions.json
    for row in data:
        for comp in filter_list:
            if row["competition_name"] == comp["competition_name"] and row["season_name"] == comp["season_name"]:
                competitions.append(row)

    if len(competitions) != len(filter_list):
        print("ERROR: couldn't find all competitions in the inclusion list.")
        return None

    return competitions

# Step 2: Get matches data from competition data
def get_matches_data(competitions_data):
    matches = []

    for comp in competitions:
        file_name = "%s.json" % comp['season_id']
        file_path = os.path.join("matches", str(comp["competition_id"]), file_name)
        data = get_json_data(file_path)
        matches.append(data)

    return matches

# Helper function to get match from the matches dict
def find_match_by_id(data, match_id):
    for season in data:
        for match in season:
            if match.get('match_id') == match_id:
                return match
    return None

# Step 3.1 get team line for a match by match_od
def get_lineups_from_match_ids(match_ids):
    lineups = {}

    for i in match_ids:
        file_name = "%s.json" % i
        file_path = os.path.join("lineups", file_name)
        data = get_json_data(file_path)
        lineups[i] = data

    return lineups

# Step 3.2 get events for match by match_id
def get_events_from_match_ids(match_ids):
    events = {}

    for i in match_ids:
        file_name = "%s.json" % i
        file_path = os.path.join("events", file_name)
        data = get_json_data(file_path)
        events[i] = data

    return events

def get_competition_data_by_id(data, competition_id):
    for comp in data:
        if comp['competition_id'] == competition_id:
            return comp
    return None

# Sanity check to make sure an ID is unique
def check_unique_id(table, unique_id):
    if(type(table) != dict and type(unique_id) != unique_id):
        print("Incorrect dict or key format")
        exit()
    if(unique_id in table):
        print("Error: key %s not unique.")
        exit()

# Deal with invalid characters that could break a query
def escape_sql_value(val):
    if isinstance(val, str):
        val = val.replace('\'', '\'\'')
        return f"'{val}'"
    elif val is None:
        return 'NULL'
    else:
        return val

# Convert the table dicts into SQL insert queries
def dict_to_sql(table_name, id_name, data_dict):
    insert_statements = ["-- Populate %s table" % table_name] # Add comment indicating table name

    for key, value in data_dict.items():
        columns = [id_name] + [col for col in value.keys()]
        values = [key] + [escape_sql_value(val) for val in value.values()]
        statement = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(str(v) for v in values)});"
        insert_statements.append(statement)

    insert_statements.append("")
    # Combine all statements into a single string separated by newlines
    return '\n'.join(insert_statements)


if __name__ == "__main__":

    # Filter out only the data we need
    # La Liga 2020/2021, 2019/2020, 2018/2019, and Premier League 2003/2004
    filter_list = [
        { "competition_name" : "La Liga", "season_name" : "2020/2021" },
        { "competition_name" : "La Liga", "season_name" : "2019/2020" },
        { "competition_name" : "La Liga", "season_name" : "2018/2019" },
        { "competition_name" : "Premier League", "season_name" : "2003/2004" },
    ]

    competitions = get_competitions_data(filter_list) # list of competition seaons
    seasons = get_matches_data(competitions) # list of seasons their matches

    # get match ids from matches
    match_ids = [match['match_id'] for season in seasons for match in season]

    lineups = get_lineups_from_match_ids(match_ids) # Get lineup data

    card_types = {
        "Yellow Card" : 0,
        "Second Yellow" : 1,
        "Red Card" : 2,
        "Other" : 3, # Shouldn't be possible but here in case
    }

    # Start gathering information for top level tables
    # t_name for data containing table data
    t_player_position = {}
    t_country = {}
    t_team = {}
    t_player = {}
    t_manager = {}
    t_stadium = {}
    t_competition_stage = {}
    t_competition = {}
    t_season = {}
    t_game_match = {}
    t_lineup_team = {}
    t_lineup_manager = {}
    t_lineup_player = {}
    t_lineup_player_position = {}
    t_lineup_player_card = {}

    t_penalty_card = {
        0 : {"card" : "Yellow Card"},
        1 : {"card" : "Second Yellow"},
        2 : {"card" : "Red Card"},
        3 : {"card" : "Other",}
    }

    # Loop through all the lineup data and populate the tables above
    for match_id in lineups:
        match_data = find_match_by_id(seasons, match_id)

        # Create competition table
        competition_id = match_data['competition']['competition_id']
        comp_data = get_competition_data_by_id(competitions, competition_id)
        competiton_row = { # TABLE:competition
            "competition_name" : match_data['competition']['competition_name'],
            # location: This can also be regions so using country isn't fitting
            "location" :  match_data['competition']['country_name'], 
            "gender" : comp_data['competition_gender'], 
            "youth" : comp_data['competition_youth'], 
            "international" : comp_data['competition_international'], 
        }
        t_competition[competition_id] = competiton_row

        # Create season table
        season_id = match_data['season']['season_id']
        season_row = { # TABLE:season
            "season_name" : match_data['season']['season_name'],
            "competition_id" : competition_id,
        }
        t_season[season_id] = season_row

        # Get home and away team ids
        home_team_id = match_data['home_team']['home_team_id']
        away_team_id = match_data['away_team']['away_team_id']

        # Get managers data and create table
        all_managers = []
        if 'managers' in match_data['home_team']:
            all_managers += match_data['home_team']['managers']

        if 'managers' in match_data['away_team']:
            all_managers += match_data['away_team']['managers']

        for manager in all_managers:
            manager_row = { # TABLE:manager
                "country_id" : manager['country']['id'],
                "manager_name" : manager['name'],
                "manager_nickname" : manager['nickname'],
                "dob" : manager['dob']
            }
            t_manager[manager['id']] = manager_row

            # Get country data and make country table
            country_id = manager['country']['id']
            country_name = manager['country']['name']
            t_country[country_id] = {"country_name" : country_name} # TABLE:country

        stadium_id = None
        # Get stadium data and create table
        if 'stadium' in match_data:
            stadium_id = match_data['stadium']['id']
            stadium_row = { # TABLE:stadium
                "stadium_name" : match_data['stadium']['name'],
                "country_id" : match_data['stadium']['country']['id']
            }
            t_stadium[stadium_id] = stadium_row

            # Redundant in case stadium's country is not prev included
            country_id = match_data['stadium']['country']['id']
            country_name = match_data['stadium']['country']['name']
            t_country[country_id] = {"country_name" : country_name} # TABLE:country

        # Get competition_stage data and create table
        competition_stage_id = match_data['competition_stage']['id']
        competition_stage_name = match_data['competition_stage']['name']
        t_competition_stage[competition_stage_id] = {"competition_stage_name" : competition_stage_name} # TABLE:competition_stage

        # Create game_match table
        game_match_row = { # TABLE:game_match
            "season_id" : match_data['season']['season_id'],
            "competition_stage_id" : competition_stage_id,
            "stadium_id" : stadium_id,
            "match_date" : match_data['match_date'],
            "match_week" : match_data['match_week'],
            "kick_off" : match_data['kick_off'],
        }
        t_game_match[match_id] = game_match_row

        for team in lineups[match_id]:
            # Get team data
            team_id = team['team_id']
            team_name = team['team_name']
            t_team[team_id] = {"team_name" : team_name} # TABLE:team
            
            team_home_away = 'home' if home_team_id == team_id else 'away'

            lineup_row = { # TABLE:lineup_team
                "match_id" : match_id,
                "team_id" : team_id,
                "score" : match_data['%s_score' % team_home_away] ,
                "home_team" : (home_team_id == team_id),
            }
            t_lineup_team_id = len(t_lineup_team) # ensures new id everytime
            check_unique_id(t_lineup_team, t_lineup_team_id) 
            t_lineup_team[t_lineup_team_id] = lineup_row

            # Get Managers and create lineup_manager table
            if 'managers' in match_data['%s_team' % team_home_away]:
                for manager in match_data['%s_team' % team_home_away]['managers']:
                    lineup_manager_row = { # TABLE:lineup_manager
                        "lineup_team_id" : t_lineup_team_id,
                        "manager_id" : manager['id']
                    }
                    t_lineup_manager_id = len(t_lineup_manager)
                    check_unique_id(t_lineup_manager, t_lineup_manager_id) 
                    t_lineup_manager[t_lineup_manager_id] = lineup_manager_row

            for player in team['lineup']:
                # Redundant in case player's country is not prev included
                country_id = player['country']['id']
                country_name = player['country']['name']
                t_country[country_id] = {"country_name" : country_name} # TABLE:country

                # Get player data and make player table
                player_id = player['player_id']
                player_row = { # TABLE:player
                    'player_name' : player['player_name'],
                    'player_nickname' : player['player_nickname'],
                    'country_id' : country_id,
                }
                t_player[player_id] = player_row

                # Create lineup_players table
                lineup_player_row = { # TABLE:lineup_player
                    "lineup_team_id" : t_lineup_team_id,
                    "player_id" : player_id,
                    "jersey_number" :  player['jersey_number']
                }
                t_lineup_player_id = len(t_lineup_player)
                check_unique_id(t_lineup_player, t_lineup_player_id) 
                t_lineup_player[t_lineup_player_id] = lineup_player_row

                # Get positions data and make table
                for position in player['positions']:
                    position_id = position['position_id']
                    position_name = position['position']
                    t_player_position[position_id] = {"position_name" : position_name} # TABLE:player_position

                    # Create player positions table
                    lineup_player_position_row = { # TABLE:lineup_player_position
                        "lineup_player_id" : t_lineup_player_id,
                        "position_id" : position_id,
                        "from_time" : position['from'],
                        "to_time" : position['to'],
                        "from_period" : position['from_period'],
                        "to_period" : position['to_period'],
                        "start_reason" : position['start_reason'],
                        "end_reason" : position['end_reason'],
                    }
                    t_lineup_player_position_id = len(t_lineup_player_position)
                    check_unique_id(t_lineup_player_position, t_lineup_player_position_id) 
                    t_lineup_player_position[t_lineup_player_position_id] = lineup_player_position_row

                # Get penalty card data and make table
                for card in player['cards']:
                    # Get id for card_type
                    card_id = card_types[card['card_type']] if card['card_type'] in card_types else card_types["Other"]

                    lineup_player_card_row = { # TABLE:lineup_player_card
                        "lineup_player_id" : t_lineup_player_id,
                        "card_type" : card_id,
                        "game_time" : card['time'],
                        "reason" : card['reason'],
                        "game_period" : card['period'],
                    }
                    t_lineup_player_card_id = len(t_lineup_player_card)
                    check_unique_id(t_lineup_player_card, t_lineup_player_card_id) 
                    t_lineup_player_card[t_lineup_player_card_id] = lineup_player_card_row

    # Convert normalized data to SQL writes
    # print(dict_to_sql("player_position", "position_id", t_player_position))
    # print(dict_to_sql("penalty_card", "card_type", t_penalty_card))
    # print(dict_to_sql("country", "country_id", t_country))
    # print(dict_to_sql("competition", "competition_id", t_competition))
    # print(dict_to_sql("season", "season_id", t_season))
    # print(dict_to_sql("team", "team_id", t_team))
    # print(dict_to_sql("player", "player_id", t_player))
    # print(dict_to_sql("manager", "manager_id", t_manager))
    # print(dict_to_sql("stadium", "stadium_id", t_stadium))
    # print(dict_to_sql("competition_stage", "competition_stage_id", t_competition_stage))
    # print(dict_to_sql("game_match", "match_id", t_game_match))
    # print(dict_to_sql("lineup_team", "lineup_team_id", t_lineup_team))
    # print(dict_to_sql("lineup_manager", "lineup_manager_id", t_lineup_manager))
    # print(dict_to_sql("lineup_player", "lineup_player_id", t_lineup_player))
    # print(dict_to_sql("lineup_player_position", "lineup_player_position_id", t_lineup_player_position))
    # print(dict_to_sql("lineup_player_card", "lineup_player_card_id", t_lineup_player_card))

    events = get_events_from_match_ids(match_ids[:1]) # Get events data

    for event in events:
        print(len(events[event]))







