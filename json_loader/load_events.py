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
        5 : {"card" : "Red Card"},
        6 : {"card" : "Second Yellow"},
        7 : {"card" : "Yellow Card"},
        0 : {"card" : "Other"}
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

        # Process data in lineups to extract all tables relevant to players & teams
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


    # events = get_events_from_match_ids(match_ids[:4]) # Get events data, reduce to smaller subset for testing
    events = get_events_from_match_ids(match_ids) # Get events data

    # General tables for event data
    t_event = {}
    t_event_type = {}
    t_play_pattern = {}
    t_related_event = {}
    t_body_part = {}
    t_outcome = {}
    t_duel_type = {}
    t_foul_type = {}

    # Dribble event tables
    t_event_14 = {}
    t_event_14_metadata = {}

    # Shot event tables
    t_event_16 = {}
    t_event_16_metadata = {}
    t_shot_type = {}
    t_shot_technique = {}

    # Pass event data
    t_event_30 = {}
    t_event_30_metadata = {}
    t_pass_type = {}
    t_pass_technique = {}
    
    # Dribbled Past event data
    t_event_39 = {}
    t_event_39_metadata = {}

    # Rest of events
    t_event_02 = {} # Ball Recovery
    t_event_03 = {} # Dispossessed
    t_event_04 = {} # Duel
    t_event_05 = {} # Camera
    t_event_06 = {} # Block
    t_event_08 = {} # Offside
    t_event_09 = {} # Clearance
    t_event_10 = {} # Interception
    t_event_17 = {} # Pressure
    t_event_18 = {} # Half Start
    t_event_19 = {} # Substitution
    t_event_20 = {} # Own Goal Against
    t_event_21 = {} # Foul Won
    t_event_22 = {} # Foul Committed
    t_event_23 = {} # Goal Keeper
    t_event_24 = {} # Bad Behaviour
    t_event_25 = {} # Own Goal For
    t_event_26 = {} # Player On
    t_event_27 = {} # Player Off
    t_event_28 = {} # Shield
    t_event_29 = {} # Camera off
    t_event_33 = {} # 50/50
    t_event_34 = {} # Half End
    t_event_35 = {} # Starting XI
    t_event_36 = {} # Tactical Shift
    t_event_37 = {} # Error
    t_event_38 = {} # Miscontrol
    t_event_40 = {} # Injury Stoppage
    t_event_41 = {} # Referee Ball-Drop
    t_event_42 = {} # Ball Receipt*
    t_event_43 = {} # Carry

    # Convert the event UUID IDs into ints, this should make look up faster and make the ID have smaller footprint 
    # This also needs to be done first so that UUID's can be converted for an event's related_events
    event_uuid_to_int_id = {} # Translates the UUID event_id to an int
    event_int_id_to_uuid = {} # Translates the event_id int to it's original UUID
    event_id_type = {} # Get the type of event
    for m_id in events:
        for event in events[m_id]:
            e_id = len(event_uuid_to_int_id) # ensures new id everytime
            check_unique_id(event_uuid_to_int_id, e_id) 
            event_uuid_to_int_id[event['id']] = e_id
            event_int_id_to_uuid[e_id] = event['id']
            event_id_type[e_id] = event['type']['id']

    # # Make sure all keys match and nothing got overwritten
    # for i in event_int_id_to_uuid:
    #     if not i == event_uuid_to_int_id[event_int_id_to_uuid[i]]:
    #         print("ERROR")

    # Now loop through all the events again and create the tables associated to events data
    for m_id in events:
        for event in events[m_id]:
            e_id = event_uuid_to_int_id[event['id']]
            e_type = event['type']['id']

            t_event_type[event['type']['id']] = {'event_type_name' : event['type']['name']} # TABLE:event_type
            t_play_pattern[event['play_pattern']['id']] = {'play_pattern_name' : event['play_pattern']['name']} # TABLE:play_pattern

            # Make entry for the event's general data,  
            event_row = { # TABLE:event
                'event_type_id': e_type,
                'event_index' :  event['index'],
                'event_period' :  event['period'],
                'event_timestamp' :  event['timestamp'],
                'play_pattern_id' :  event['play_pattern']['id'],
                'possession' : event['possession']
            }
            t_event[e_id] = event_row

            # Create rows for the event's related_events
            if 'related_events' in event:
                for i in event['related_events']:
                    related_event_row = { # TABLE:related_event
                        'original_event' : e_id,
                        'original_event_type_id' : e_type,
                        'related_id' : event_uuid_to_int_id[i],
                        'related_type_id' : event_id_type[event_uuid_to_int_id[i]]
                    }
                    t_related_event_id = len(t_related_event)
                    check_unique_id(t_related_event, t_related_event_id) 
                    t_related_event[t_related_event_id] = related_event_row

            if e_type == 14: # Populate event_14 table for dribble event
                event_14_row = { # TABLE:event_14
                    'event_id' : e_id,
                    'match_id' : m_id,
                    'player_id' : event['player']['id'],
                    'team_id' : event['team']['id'],
                    'complete' : event['dribble']['outcome']['name'] == "Complete"
                }
                t_event_14_id = len(t_event_14)
                check_unique_id(t_event_14, t_event_14_id) 
                t_event_14[t_event_14_id] = event_14_row

                event_14_metadata_row = {
                    'event_14_id' : t_event_14_id, # int (event_14 FK)
                    'location_x' : event['location'][0], # float
                    'location_y' : event['location'][1], # float
                    'duration' : event['duration'], # float
                }
                t_event_14_metadata_id = len(t_event_14_metadata)
                check_unique_id(t_event_14_metadata, t_event_14_metadata_id) 
                t_event_14_metadata[t_event_14_metadata_id] = event_14_metadata_row

            elif e_type == 16: # Populate event_16 table for shot event
                event_16_row = { # TABLE:event_16
                    'event_id' : e_id,
                    'match_id' : m_id,
                    'player_id' : event['player']['id'],
                    'team_id' : event['team']['id'],
                    'xg_score' : event['shot']['statsbomb_xg'],
                    'first_time' : 'first_time' in event['shot'] and event['shot']['first_time'] == True
                }
                t_event_16_id = len(t_event_16)
                check_unique_id(t_event_16, t_event_16_id) 
                t_event_16[t_event_16_id] = event_16_row

                shot_id = event['shot']['type']['id']
                t_shot_type[shot_id] = {'shot_type_name' : event['shot']['type']['name']} # TABLE:shot_type
                
                outcome_id = event['shot']['outcome']['id']
                t_outcome[outcome_id] = {'outcome_name' : event['shot']['outcome']['name']} # TABLE:outcome

                technique_id = event['shot']['technique']['id']
                t_shot_technique[technique_id] = {'shot_technique_name' : event['shot']['technique']['name']} # TABLE:outcome

                bp_id = event['shot']['body_part']['id']
                t_body_part[bp_id] = {'body_part_name' : event['shot']['body_part']['name']} # TABLE:body_part

                loc_x = None
                loc_y = None
                if 'end_location' in event['shot']:
                    loc_x = event['shot']['end_location'][0]
                    loc_y = event['shot']['end_location'][1]

                deflected = 'deflected' in event and event['shot']['deflected']
                one_on_one = 'one_on_one' in event and event['shot']['one_on_one']
                aerial_won = 'aerial_won' in event and event['shot']['aerial_won']
                saved_to_post = 'saved_to_post' in event and event['shot']['saved_to_post']
                redirect = 'redirect' in event and event['shot']['redirect']
                open_goal = 'open_goal' in event and event['shot']['open_goal']
                follows_dribble = 'follows_dribble' in event and event['shot']['follows_dribble']
                saved_off_target = 'saved_off_target' in event and event['shot']['saved_off_target']

                event_16_metadata_row = {
                    'event_16_id' : t_event_16_id, # int (event_16 FK)
                    'location_x' : event['location'][0], # float
                    'location_y' : event['location'][1], # float
                    'duration' : event['duration'], # float
                    'shot_type_id' : shot_id, # int (shot_type FK)
                    'outcome_id' : outcome_id, # int (outcome FK)
                    'shot_technique_id' : technique_id, # int (shot_technique FK)
                    'body_part_id' : bp_id, # int (body_part FK)
                    'end_location_x' :  loc_x, # float
                    'end_location_y' : loc_y, # float 
                    'deflected' : deflected, # bool
                    'one_on_one' : one_on_one, # bool
                    'aerial_won' : aerial_won, # bool
                    'saved_to_post' : saved_to_post, # bool
                    'redirect' : redirect, # bool
                    'open_goal' : open_goal, # bool
                    'follows_dribble' : follows_dribble, # bool
                    'saved_off_target' : saved_off_target, # bool
                }
                t_event_16_metadata_id = len(t_event_16_metadata)
                check_unique_id(t_event_16_metadata, t_event_16_metadata_id) 
                t_event_16_metadata[t_event_16_metadata_id] = event_16_metadata_row

            elif e_type == 30: # Populate event_30 table for pass event

                # Get pass type, this field doesn't always exist so it'll be filled later
                # p_type = None
                # if 'type' in event['pass']:
                #     p_type = event['pass']['type']['id']
                #     t_pass_type[p_type] = {'pass_type_name' : event['pass']['type']['name']} # TABLE:pass_type

                through_ball =  False
                if('through_ball' in event['pass']):
                    through_ball = event['pass']['through_ball']

                # Get recipient if there is one
                recipient = None
                if 'recipient' in event['pass']:
                    recipient = event['pass']['recipient']['id']

                event_30_row = { # TABLE:event_30
                    'event_id' : e_id,
                    'match_id' : m_id,
                    'player_id' : event['player']['id'],
                    'team_id' : event['team']['id'],
                    'recipient_id' : recipient,
                    'through_ball' : through_ball
                    # 'pass_type_id' : p_type
                }
                t_event_30_id = len(t_event_30)
                check_unique_id(t_event_30, t_event_30_id) 
                t_event_30[t_event_30_id] = event_30_row

                pass_id = None
                if 'type' in event['pass']:
                    pass_id = event['pass']['type']['id']
                    t_pass_type[pass_id] = {'pass_type_name' : event['pass']['type']['name']} # TABLE:pass_type
                
                outcome_id = None
                if 'outcome' in event['pass']: 
                    outcome_id = event['pass']['outcome']['id']
                    t_outcome[outcome_id] = {'outcome_name' : event['pass']['outcome']['name']} # TABLE:outcome

                technique_id = None
                if 'technique' in event['pass']:
                    technique_id = event['pass']['technique']['id']
                    t_pass_technique[technique_id] = {'pass_technique_name' : event['pass']['technique']['name']} # TABLE:outcome

                loc_x = None
                loc_y = None
                if 'end_location' in event['pass']:
                    loc_x = event['pass']['end_location'][0]
                    loc_y = event['pass']['end_location'][1]

                bp_id = None
                if 'body_part' in event['pass']:
                    bp_id = event['pass']['body_part']['id']
                    t_body_part[bp_id] = {'body_part_name' : event['pass']['body_part']['name']} # TABLE:body_part
                
                deflected = 'deflected' in event and event['pass']['deflected']
                aerial_won = 'aerial_won' in event and event['pass']['aerial_won']
                shot_assist = 'shot_assist' in event and event['pass']['shot_assist']
                switch = 'switch' in event and event['pass']['switch']
                cross = 'cross' in event and event['pass']['cross']
                deflected = 'deflected' in event and event['pass']['deflected']
                inswinging = 'inswinging' in event and event['pass']['inswinging']
                through_ball = 'through_ball' in event and event['pass']['through_ball']
                no_touch = 'no_touch' in event and event['pass']['no_touch']
                outswinging = 'outswinging' in event and event['pass']['outswinging']
                miscommunication = 'miscommunication' in event and event['pass']['miscommunication']
                cut_back = 'cut_back' in event and event['pass']['cut_back']
                goal_assist = 'goal_assist' in event and event['pass']['goal_assist']
                straight = 'straight' in event and event['pass']['straight']

                event_30_metadata_row = {
                    'event_30_id' : t_event_30_id, # int (event_30 FK)
                    'location_x' : event['location'][0], # float
                    'location_y' : event['location'][1], # float
                    'duration' : event['duration'], # float
                    'length' : event['pass']['length'], # float
                    'angle' : event['pass']['angle'], # float
                    'pass_type_id' : pass_id, # int (pass_type FK)
                    'outcome_id' : outcome_id, # int (outcome FK)
                    'pass_technique_id' : technique_id, # int (pass_technique FK)
                    'body_part_id' : bp_id, # int (body_part FK)
                    'end_location_x' :  loc_x, # float
                    'end_location_y' : loc_y, # float
                    'aerial_won' : aerial_won, # bool
                    'shot_assist' : shot_assist, # bool
                    'pass_switch' : switch, # bool
                    'pass_cross' : cross, # bool
                    'deflected' : deflected, # bool
                    'inswinging' : inswinging, # bool
                    'through_ball' : through_ball, # bool
                    'no_touch' : no_touch, # bool
                    'outswinging' : outswinging, # bool
                    'miscommunication' : miscommunication, # bool
                    'cut_back' : cut_back, # bool
                    'goal_assist' : goal_assist, # bool
                    'straight' : straight, # bool 
                }
                t_event_30_metadata_id = len(t_event_30_metadata)
                check_unique_id(t_event_30_metadata, t_event_30_metadata_id) 
                t_event_30_metadata[t_event_30_metadata_id] = event_30_metadata_row

            elif e_type == 39: # Populate event_39 for Dribbled Past event
                event_14_id = None
                if 'related_events' in event:
                    for i in event['related_events']:
                        if event_id_type[event_uuid_to_int_id[i]] == 14:
                            event_general_id = event_uuid_to_int_id[i] # Convert UUID to general event ID

                event_39_row = { # TABLE:event_39
                    'event_id' : e_id,
                    'match_id' : m_id,
                    'player_id' : event['player']['id'],
                    'team_id' : event['team']['id'],
                    'event_14_id' : event_general_id, # Convert event_id to event_14_id later
                    'completed_dribble' : None # Look this up later in the related event_14 data
                }
                t_event_39_id = len(t_event_39)
                check_unique_id(t_event_39, t_event_39_id) 
                t_event_39[t_event_39_id] = event_39_row

                event_39_metadata_row = {
                    'event_39_id' : t_event_39_id, # int (event_39 FK)
                    'location_x' : event['location'][0], # float
                    'location_y' : event['location'][1], # float
                    'duration' : event['duration'], # float
                }
                t_event_39_metadata_id = len(t_event_39_metadata)
                check_unique_id(t_event_39_metadata, t_event_39_metadata_id) 
                t_event_39_metadata[t_event_39_metadata_id] = event_39_metadata_row

            # Start making tables for the other event types
            elif e_type == 2: # Ball Recovery
                event_02_row = {
                    'event_id' : e_id, # int (event FK)
                    'match_id' : m_id, # int (game_match FK)
                    'player_id' : event['player']['id'], # int (player FK)
                    'team_id' : event['team']['id'], # int (team FK)
                    'location_x' : event['location'][0], # float
                    'location_y' : event['location'][1], # float
                    'duration' : event['duration'], # float
                }
                t_event_02_id = len(t_event_02)
                check_unique_id(t_event_02, t_event_02_id) 
                t_event_02[t_event_02_id] = event_02_row

            elif e_type == 3: # Dispossessed
                event_03_row = {
                    'event_id' : e_id, # int (event FK)
                    'match_id' : m_id, # int (game_match FK)
                    'player_id' : event['player']['id'], # int (player FK)
                    'team_id' : event['team']['id'], # int (team FK)
                    'location_x' : event['location'][0], # float
                    'location_y' : event['location'][1], # float
                    'duration' : event['duration'], # float
                }
                t_event_03_id = len(t_event_03)
                check_unique_id(t_event_03, t_event_03_id) 
                t_event_03[t_event_03_id] = event_03_row

            elif e_type == 4: # Duel
                #@@
                duel_id = event['duel']['type']['id']
                t_duel_type[duel_id] = {'duel_type_name' : event['duel']['type']['name']} # TABLE:duel_type
                
                outcome_id = None
                if 'outcome' in event['duel']:
                    outcome_id = event['duel']['outcome']['id']
                    t_outcome[outcome_id] = {'outcome_name' : event['duel']['outcome']['name']} # TABLE:outcome


                event_04_row = {
                    'event_id' : e_id, # int (event FK)
                    'match_id' : m_id, # int (game_match FK)
                    'player_id' : event['player']['id'], # int (player FK)
                    'team_id' : event['team']['id'], # int (team FK)
                    'location_x' : event['location'][0], # float
                    'location_y' : event['location'][1], # float
                    'duration' : event['duration'], # float
                    'duel_type_id' : duel_id, # int (duel_type FK)
                    'outcome_id' : outcome_id, # int, can be null (outcome FK)
                }
                t_event_04_id = len(t_event_04)
                check_unique_id(t_event_04, t_event_04_id) 
                t_event_04[t_event_04_id] = event_04_row

            elif e_type == 5: # Camera On
                event_05_row = {
                    'event_id' : e_id, # int (event FK)
                    'match_id' : m_id, # int (game_match FK)
                    'player_id' : event['player']['id'], # int (player FK)
                    'team_id' : event['team']['id'], # int (team FK)
                }
                t_event_05_id = len(t_event_05)
                check_unique_id(t_event_05, t_event_05_id) 
                t_event_05[t_event_05_id] = event_05_row

            elif e_type == 6: # Block
                deflection = False
                offensive = False
                save_block = False

                if 'block' in event:
                    if 'deflection' in event['block']:
                        deflection = event['block']['deflection']
                    if 'offensive' in event['block']:
                        offensive = event['block']['offensive']
                    if 'save_block' in event['block']:
                        save_block = event['block']['save_block']

                event_06_row = {
                    'event_id' : e_id, # int (event FK)
                    'match_id' : m_id, # int (game_match FK)
                    'player_id' : event['player']['id'], # int (player FK)
                    'team_id' : event['team']['id'], # int (team FK)
                    'location_x' : event['location'][0], # float
                    'location_y' : event['location'][1], # float
                    'duration' : event['duration'], # float
                    'deflection' : deflection, # bool
                    'offensive' : offensive, # bool
                    'save_block' : save_block, # bool
                }
                t_event_06_id = len(t_event_06)
                check_unique_id(t_event_06, t_event_06_id) 
                t_event_06[t_event_06_id] = event_06_row

            elif e_type == 8: # Offside
                event_08_row = {
                    'event_id' : e_id, # int (event FK)
                    'match_id' : m_id, # int (game_match FK)
                    'player_id' : event['player']['id'], # int (player FK)
                    'team_id' : event['team']['id'], # int (team FK)
                    'location_x' : event['location'][0], # float
                    'location_y' : event['location'][1], # float
                    'duration' : event['duration'], # float
                }
                t_event_08_id = len(t_event_08)
                check_unique_id(t_event_08, t_event_08_id) 
                t_event_08[t_event_08_id] = event_08_row

            elif e_type == 9: # Clearance
                bp_id = event['clearance']['body_part']['id']
                t_body_part[bp_id] = {'body_part_name' : event['clearance']['body_part']['name']} # TABLE:body_part

                event_09_row = {
                    'event_id' : e_id, # int (event FK)
                    'match_id' : m_id, # int (game_match FK)
                    'player_id' : event['player']['id'], # int (player FK)
                    'team_id' : event['team']['id'], # int (team FK)
                    'location_x' : event['location'][0], # float
                    'location_y' : event['location'][1], # float
                    'duration' : event['duration'], # float
                    'aerial_won' : 'aerial_won' in event['clearance'] and event['clearance']['aerial_won'], # bool
                    'body_part_id' : bp_id, # int (body_part FK)
                }
                t_event_09_id = len(t_event_09)
                check_unique_id(t_event_09, t_event_09_id) 
                t_event_09[t_event_09_id] = event_09_row

            elif e_type == 10: # Interception
                outcome_id = event['interception']['outcome']['id']
                t_outcome[outcome_id] = {'outcome_name' : event['interception']['outcome']['name']} # TABLE:outcome

                event_10_row = {
                    'event_id' : e_id, # int (event FK)
                    'match_id' : m_id, # int (game_match FK)
                    'player_id' : event['player']['id'], # int (player FK)
                    'team_id' : event['team']['id'], # int (team FK)
                    'location_x' : event['location'][0], # float
                    'location_y' : event['location'][1], # float
                    'duration' : event['duration'], # float
                    'outcome_id' : outcome_id, # int (outcome FK)
                }
                t_event_10_id = len(t_event_10)
                check_unique_id(t_event_10, t_event_10_id) 
                t_event_10[t_event_10_id] = event_10_row

            elif e_type == 17: # Pressure
                event_17_row = {
                    'event_id' : e_id, # int (event FK)
                    'match_id' : m_id, # int (game_match FK)
                    'player_id' : event['player']['id'], # int (player FK)
                    'team_id' : event['team']['id'], # int (team FK)
                    'location_x' : event['location'][0], # float
                    'location_y' : event['location'][1], # float
                    'duration' : event['duration'], # float
                    'counterpress' : 'counterpress' in event and event['counterpress'] , # bool
                }
                t_event_17_id = len(t_event_17)
                check_unique_id(t_event_17, t_event_17_id) 
                t_event_17[t_event_17_id] = event_17_row

            elif e_type == 18: # Half Start
                event_18_row = {
                    'event_id' : e_id, # int (event FK)
                    'match_id' : m_id, # int (game_match FK)
                    'duration' : event['duration'], # float
                    'late_video_start' : 'half_start' in event and event['half_start']['late_video_start'], # bool
                }
                t_event_18_id = len(t_event_18)
                check_unique_id(t_event_18, t_event_18_id) 
                t_event_18[t_event_18_id] = event_18_row

            elif e_type == 19: # Substitution
                outcome_id = event['substitution']['outcome']['id']
                t_outcome[outcome_id] = {'outcome_name' : event['substitution']['outcome']['name']} # TABLE:outcome

                event_19_row = {
                    'event_id' : e_id, # int (event FK)
                    'match_id' : m_id, # int (game_match FK)
                    'player_id' : event['player']['id'], # int (player FK)
                    'team_id' : event['team']['id'], # int (team FK)
                    'duration' : event['duration'], # float
                    'outcome_id' : outcome_id, # int (outcome FK)
                    'replacement_id' : event['substitution']['replacement']['id'], # int, (player FK)
                }
                t_event_19_id = len(t_event_19)
                check_unique_id(t_event_19, t_event_19_id) 
                t_event_19[t_event_19_id] = event_19_row

            elif e_type == 20: # Own Goal Against
                event_20_row = {
                    'event_id' : e_id, # int (event FK)
                    'match_id' : m_id, # int (game_match FK)
                    'player_id' : event['player']['id'], # int (player FK)
                    'team_id' : event['team']['id'], # int (team FK)
                    'location_x' : event['location'][0], # float
                    'location_y' : event['location'][1], # float
                    'duration' : event['duration'], # float
                }
                t_event_20_id = len(t_event_20)
                check_unique_id(t_event_20, t_event_20_id) 
                t_event_20[t_event_20_id] = event_20_row

            elif e_type == 21: # Foul Won
                penalty = False
                defensive = False
                advantage = False

                if 'foul_won' in event:
                    if 'penalty' in event['foul_won']:
                        penalty = event['foul_won']['penalty']
                    if 'defensive' in event['foul_won']:
                        defensive = event['foul_won']['defensive']
                    if 'advantage' in event['foul_won']:
                        advantage = event['foul_won']['advantage']

                event_21_row = {
                    'event_id' : e_id, # int (event FK)
                    'match_id' : m_id, # int (game_match FK)
                    'player_id' : event['player']['id'], # int (player FK)
                    'team_id' : event['team']['id'], # int (team FK)
                    'location_x' : event['location'][0], # float
                    'location_y' : event['location'][1], # float
                    'duration' : event['duration'], # float
                    'penalty' : penalty, # bool
                    'defensive' : defensive, # bool
                    'advantage' : advantage, # bool
                }
                t_event_21_id = len(t_event_21)
                check_unique_id(t_event_21, t_event_21_id) 
                t_event_21[t_event_21_id] = event_21_row

            elif e_type == 22: # Foul Committed
                penalty = False
                advantage = False
                offensive = False
                card = None
                foul_id = None

                if 'foul_committed' in event:
                    card = None
                    if 'card' in event['foul_committed']:
                        card = event['foul_committed']['card']['id']

                    foul_id = None
                    if 'type' in event['foul_committed']:
                        #@@
                        foul_id = event['foul_committed']['type']['id']
                        t_foul_type[foul_id] = {'foul_type_name' : event['foul_committed']['type']['name']} # TABLE:foul_type

                event_22_row = {
                    'event_id' : e_id, # int (event FK)
                    'match_id' : m_id, # int (game_match FK)
                    'player_id' : event['player']['id'], # int (player FK)
                    'team_id' : event['team']['id'], # int (team FK)
                    'location_x' : event['location'][0], # float
                    'location_y' : event['location'][1], # float
                    'duration' : event['duration'], # float
                    'penalty' : penalty, # bool
                    'advantage' : advantage, # bool
                    'offensive' : offensive, # bool
                    'penalty_card_id' : card, # int, can be null (penalty_card FK)
                    'foul_id' : foul_id, # int, can be null (foul_type FK)
                }
                t_event_22_id = len(t_event_22)
                check_unique_id(t_event_22, t_event_22_id) 
                t_event_22[t_event_22_id] = event_22_row

            elif e_type == 23: # Goal Keeper #@@
                loc_x = None
                loc_y = None
                if 'location' in event:
                    loc_x = event['location'][0]
                    loc_y = event['location'][1]

                event_23_row = {
                    'event_id' : e_id, # int (event FK)
                    'match_id' : m_id, # int (game_match FK)
                    'player_id' : event['player']['id'], # int (player FK)
                    'team_id' : event['team']['id'], # int (team FK)
                    'location_x' : loc_x, # float
                    'location_y' : loc_y, # float
                    'duration' : event['duration'], # float
                }
                t_event_23_id = len(t_event_23)
                check_unique_id(t_event_23, t_event_23_id) 
                t_event_23[t_event_23_id] = event_23_row

            elif e_type == 24: # Bad Behaviour
                event_24_row = {
                    'event_id' : e_id, # int (event FK)
                    'match_id' : m_id, # int (game_match FK)
                    'player_id' : event['player']['id'], # int (player FK)
                    'team_id' : event['team']['id'], # int (team FK)
                    'duration' : event['duration'], # float
                    'penalty_card_id' : event['bad_behaviour']['card']['id']
                }
                t_event_24_id = len(t_event_24)
                check_unique_id(t_event_24, t_event_24_id) 
                t_event_24[t_event_24_id] = event_24_row

            elif e_type == 25: # Own Goal For

                player_id = None
                if 'player' in event:
                    player_id = event['player']['id']

                event_25_row = {
                    'event_id' : e_id, # int (event FK)
                    'match_id' : m_id, # int (game_match FK)
                    'player_id' : player_id, # int (player FK)
                    'team_id' : event['team']['id'], # int (team FK)
                    'location_x' : event['location'][0], # float
                    'location_y' : event['location'][1], # float
                    'duration' : event['duration'], # float
                }
                t_event_25_id = len(t_event_25)
                check_unique_id(t_event_25, t_event_25_id) 
                t_event_25[t_event_25_id] = event_25_row

            elif e_type == 26: # Player On
                event_26_row = {
                    'event_id' : e_id, # int (event FK)
                    'match_id' : m_id, # int (game_match FK)
                    'player_id' : event['player']['id'], # int (player FK)
                    'team_id' : event['team']['id'], # int (team FK)
                    'duration' : event['duration'], # float
                }
                t_event_26_id = len(t_event_26)
                check_unique_id(t_event_26, t_event_26_id) 
                t_event_26[t_event_26_id] = event_26_row

            elif e_type == 27: # Player Off
                event_27_row = {
                    'event_id' : e_id, # int (event FK)
                    'match_id' : m_id, # int (game_match FK)
                    'player_id' : event['player']['id'], # int (player FK)
                    'team_id' : event['team']['id'], # int (team FK)
                    'duration' : event['duration'], # float
                }
                t_event_27_id = len(t_event_27)
                check_unique_id(t_event_27, t_event_27_id) 
                t_event_27[t_event_27_id] = event_27_row

            elif e_type == 28: # Shield
                event_28_row = {
                    'event_id' : e_id, # int (event FK)
                    'match_id' : m_id, # int (game_match FK)
                    'player_id' : event['player']['id'], # int (player FK)
                    'team_id' : event['team']['id'], # int (team FK)
                    'location_x' : event['location'][0], # float
                    'location_y' : event['location'][1], # float
                    'duration' : event['duration'], # float
                }
                t_event_28_id = len(t_event_28)
                check_unique_id(t_event_28, t_event_28_id) 
                t_event_28[t_event_28_id] = event_28_row

            elif e_type == 29: # Camera off
                event_29_row = {
                    'event_id' : e_id, # int (event FK)
                    'match_id' : m_id, # int (game_match FK)
                    'player_id' : event['player']['id'], # int (player FK)
                    'team_id' : event['team']['id'], # int (team FK)
                    'location_x' : event['location'][0], # float
                    'location_y' : event['location'][1], # float
                    'duration' : event['duration'], # float
                }
                t_event_29_id = len(t_event_29)
                check_unique_id(t_event_29, t_event_29_id) 
                t_event_29[t_event_29_id] = event_29_row

            elif e_type == 33: # 50/50
                outcome_id = None
                if 'outcome' in event['50_50']:
                    outcome_id = event['50_50']['outcome']['id']
                    t_outcome[outcome_id] = {'outcome_name' : event['50_50']['outcome']['name']} # TABLE:outcome

                event_33_row = {
                    'event_id' : e_id, # int (event FK)
                    'match_id' : m_id, # int (game_match FK)
                    'player_id' : event['player']['id'], # int (player FK)
                    'team_id' : event['team']['id'], # int (team FK)
                    'location_x' : event['location'][0], # float
                    'location_y' : event['location'][1], # float
                    'duration' : event['duration'], # float,
                    'outcome_id' : outcome_id, # int (outcome FK)
                }
                t_event_33_id = len(t_event_33)
                check_unique_id(t_event_33, t_event_33_id) 
                t_event_33[t_event_33_id] = event_33_row

            elif e_type == 34: # Half End
                event_34_row = {
                    'event_id' : e_id, # int (event FK)
                    'match_id' : m_id, # int (game_match FK)
                    'team_id' : event['team']['id'], # int (team FK)
                    'duration' : event['duration'], # float
                }
                t_event_34_id = len(t_event_34)
                check_unique_id(t_event_34, t_event_34_id) 
                t_event_34[t_event_34_id] = event_34_row

            elif e_type == 35: # Starting XI #@@
                event_35_row = {
                    'event_id' : e_id, # int (event FK)
                    'match_id' : m_id, # int (game_match FK)
                    'team_id' : event['team']['id'], # int (team FK)
                    'duration' : event['duration'], # float
                }
                t_event_35_id = len(t_event_35)
                check_unique_id(t_event_35, t_event_35_id) 
                t_event_35[t_event_35_id] = event_35_row

            elif e_type == 36: # Tactical Shift #@@
                event_36_row = {
                    'event_id' : e_id, # int (event FK)
                    'match_id' : m_id, # int (game_match FK)
                    'team_id' : event['team']['id'], # int (team FK)
                    'duration' : event['duration'], # float
                }
                t_event_36_id = len(t_event_36)
                check_unique_id(t_event_36, t_event_36_id) 
                t_event_36[t_event_36_id] = event_36_row

            elif e_type == 37: # Error
                event_37_row = {
                    'event_id' : e_id, # int (event FK)
                    'match_id' : m_id, # int (game_match FK)
                    'player_id' : event['player']['id'], # int (player FK)
                    'team_id' : event['team']['id'], # int (team FK)
                    'location_x' : event['location'][0], # float
                    'location_y' : event['location'][1], # float
                    'duration' : event['duration'], # float
                }
                t_event_37_id = len(t_event_37)
                check_unique_id(t_event_37, t_event_37_id) 
                t_event_37[t_event_37_id] = event_37_row

            elif e_type == 38: # Miscontrol
                aerial_won = False
                if 'miscontrol' in event:
                    aerial_won = event['miscontrol']['aerial_won']

                event_38_row = {
                    'event_id' : e_id, # int (event FK)
                    'match_id' : m_id, # int (game_match FK)
                    'player_id' : event['player']['id'], # int (player FK)
                    'team_id' : event['team']['id'], # int (team FK)
                    'location_x' : event['location'][0], # float
                    'location_y' : event['location'][1], # float
                    'duration' : event['duration'], # float
                    'aerial_won' : aerial_won, # bool
                }
                t_event_38_id = len(t_event_38)
                check_unique_id(t_event_38, t_event_38_id) 
                t_event_38[t_event_38_id] = event_38_row

            elif e_type == 40: # Injury Stoppage
                in_chain = False
                if 'injury_stoppage' in event:
                    in_chain = event['injury_stoppage']['in_chain']

                loc_x = None
                loc_y = None
                if 'location' in event:
                    loc_x = event['location'][0]
                    loc_y = event['location'][1]

                event_40_row = {
                    'event_id' : e_id, # int (event FK)
                    'match_id' : m_id, # int (game_match FK)
                    'player_id' : event['player']['id'], # int (player FK)
                    'team_id' : event['team']['id'], # int (team FK)
                    'location_x' : loc_x, # float
                    'location_y' : loc_y, # float
                    'duration' : event['duration'], # float
                    'in_chain' : in_chain, #bool
                }
                t_event_40_id = len(t_event_40)
                check_unique_id(t_event_40, t_event_40_id) 
                t_event_40[t_event_40_id] = event_40_row

            elif e_type == 41: # Referee Ball-Drop
                event_41_row = {
                    'event_id' : e_id, # int (event FK)
                    'match_id' : m_id, # int (game_match FK)
                    'team_id' : event['team']['id'], # int (team FK)
                    'location_x' : event['location'][0], # float
                    'location_y' : event['location'][1], # float
                    'duration' : event['duration'], # float
                }
                t_event_41_id = len(t_event_41)
                check_unique_id(t_event_41, t_event_41_id) 
                t_event_41[t_event_41_id] = event_41_row

            elif e_type == 42: # Ball Receipt*
                outcome_id = None
                if 'ball_receipt' in event:
                    outcome_id = event['ball_receipt']['outcome']['id']
                    t_outcome[outcome_id] = {'outcome_name' : event['ball_receipt']['outcome']['name']} # TABLE:outcome


                event_42_row = {
                    'event_id' : e_id, # int (event FK)
                    'match_id' : m_id, # int (game_match FK)
                    'player_id' : event['player']['id'], # int (player FK)
                    'team_id' : event['team']['id'], # int (team FK)
                    'location_x' : event['location'][0], # float
                    'location_y' : event['location'][1], # float
                    'outcome_id' : outcome_id, # int (outcome FK)
                }
                t_event_42_id = len(t_event_42)
                check_unique_id(t_event_42, t_event_42_id) 
                t_event_42[t_event_42_id] = event_42_row

            elif e_type == 43: # Carry
                event_43_row = {
                    'event_id' : e_id, # int (event FK)
                    'match_id' : m_id, # int (game_match FK)
                    'player_id' : event['player']['id'], # int (player FK)
                    'team_id' : event['team']['id'], # int (team FK)
                    'location_x' : event['location'][0], # float
                    'location_y' : event['location'][1], # float
                    'end_location_x' : event['carry']['end_location'][0], # float
                    'end_location_y' : event['carry']['end_location'][1], # float
                    'duration' : event['duration'], # float
                }
                t_event_43_id = len(t_event_43)
                check_unique_id(t_event_43, t_event_43_id) 
                t_event_43[t_event_43_id] = event_43_row


    # Update event_39 (Dribbled Past events) with relevant info from event_14 (Dribble)
    for e39_id in t_event_39:
        for e14_id in t_event_14:
            if t_event_39[e39_id]['event_14_id'] == t_event_14[e14_id]['event_id']:
                t_event_39[e39_id]['event_14_id'] = e14_id # Find and replace the event_id with it's event_14_id
                t_event_39[e39_id]['completed_dribble'] = t_event_14[e14_id]['complete']

    # Convert normalized data to SQL writes

    # # Player, Team and Match Data
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

    # Top level
    print(dict_to_sql("outcome", "outcome_id", t_outcome))
    print(dict_to_sql("body_part", "body_part_id", t_body_part))
    print(dict_to_sql("duel_type", "duel_type_id", t_duel_type))
    print(dict_to_sql("foul_type", "foul_type_id", t_foul_type))
    print(dict_to_sql("shot_type", "shot_type_id", t_shot_type))
    print(dict_to_sql("shot_technique", "shot_technique_id", t_shot_technique))
    print(dict_to_sql("pass_type", "pass_type_id", t_pass_type))
    print(dict_to_sql("pass_technique", "pass_technique_id", t_pass_technique))

    # # Main Events Data 
    # print(dict_to_sql("event_type", "event_type_id", t_event_type))
    # print(dict_to_sql("play_pattern", "play_pattern_id", t_play_pattern))
    # print(dict_to_sql("pass_type", "pass_type_id", t_pass_type))
    # print(dict_to_sql("event", "event_id", t_event))
    # print(dict_to_sql("event_14", "event_14_id", t_event_14))
    # print(dict_to_sql("event_16", "event_16_id", t_event_16))
    # print(dict_to_sql("event_30", "event_30_id", t_event_30))
    # print(dict_to_sql("event_39", "event_39_id", t_event_39))

    # Event Metadata Tables
    print(dict_to_sql("event_14_metadata", "event_14_metadata_id", t_event_14_metadata))
    print(dict_to_sql("event_16_metadata", "event_16_metadata_id", t_event_16_metadata))
    print(dict_to_sql("event_30_metadata", "event_30_metadata_id", t_event_30_metadata))
    print(dict_to_sql("event_39_metadata", "event_39_metadata_id", t_event_39_metadata))

    # Other Events Data
    print(dict_to_sql("event_02", "event_02_id", t_event_02))
    print(dict_to_sql("event_03", "event_03_id", t_event_03))
    print(dict_to_sql("event_04", "event_04_id", t_event_04))
    print(dict_to_sql("event_05", "event_05_id", t_event_05))
    print(dict_to_sql("event_06", "event_06_id", t_event_06))
    print(dict_to_sql("event_08", "event_08_id", t_event_08))
    print(dict_to_sql("event_09", "event_09_id", t_event_09))
    print(dict_to_sql("event_10", "event_10_id", t_event_10))
    print(dict_to_sql("event_17", "event_17_id", t_event_17))
    print(dict_to_sql("event_18", "event_18_id", t_event_18))
    print(dict_to_sql("event_19", "event_19_id", t_event_19))
    print(dict_to_sql("event_20", "event_20_id", t_event_20))
    print(dict_to_sql("event_21", "event_21_id", t_event_21))
    print(dict_to_sql("event_22", "event_22_id", t_event_22))
    print(dict_to_sql("event_23", "event_23_id", t_event_23))
    print(dict_to_sql("event_24", "event_24_id", t_event_24))
    print(dict_to_sql("event_25", "event_25_id", t_event_25))
    print(dict_to_sql("event_26", "event_26_id", t_event_26))
    print(dict_to_sql("event_27", "event_27_id", t_event_27))
    print(dict_to_sql("event_28", "event_28_id", t_event_28))
    print(dict_to_sql("event_29", "event_29_id", t_event_29))
    print(dict_to_sql("event_33", "event_33_id", t_event_33))
    print(dict_to_sql("event_34", "event_34_id", t_event_34))
    print(dict_to_sql("event_35", "event_35_id", t_event_35))
    print(dict_to_sql("event_36", "event_36_id", t_event_36))
    print(dict_to_sql("event_37", "event_37_id", t_event_37))
    print(dict_to_sql("event_38", "event_38_id", t_event_38))
    print(dict_to_sql("event_40", "event_40_id", t_event_40))
    print(dict_to_sql("event_41", "event_41_id", t_event_41))
    print(dict_to_sql("event_42", "event_42_id", t_event_42))
    print(dict_to_sql("event_43", "event_43_id", t_event_43))




