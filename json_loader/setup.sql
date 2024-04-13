CREATE TABLE country (
    country_id INTEGER PRIMARY KEY,
    country_name VARCHAR(50) NOT NULL
);

CREATE TABLE player (
    player_id INTEGER PRIMARY KEY,
    player_name VARCHAR(50) NOT NULL,
    player_nickname VARCHAR(50),
    country_id INTEGER REFERENCES country(country_id)
);

CREATE TABLE manager (
    manager_id INTEGER PRIMARY KEY,
    manager_name VARCHAR(50) NOT NULL,
    manager_nickname VARCHAR(50),
    dob DATE,
    country_id INTEGER REFERENCES country(country_id)
);

CREATE TABLE stadium (
    stadium_id INTEGER PRIMARY KEY,
    stadium_name VARCHAR(50) NOT NULL,
    country_id INTEGER REFERENCES country(country_id)
);

CREATE TABLE competition_stage (
    competition_stage_id INTEGER PRIMARY KEY,
    competition_stage_name VARCHAR(50) NOT NULL
);

CREATE TABLE competition (
    competition_id INTEGER PRIMARY KEY,
    competition_name VARCHAR(50) NOT NULL,
    location VARCHAR(50),
    gender VARCHAR(10),
    youth BOOLEAN,
    international BOOLEAN
);

CREATE TABLE season (
    season_id INTEGER PRIMARY KEY,
    season_name VARCHAR(50) NOT NULL,
    competition_id INTEGER REFERENCES competition(competition_id)
);

CREATE TABLE game_match (
    match_id INTEGER PRIMARY KEY,
    season_id INTEGER REFERENCES season(season_id),
    competition_stage_id INTEGER REFERENCES competition_stage(competition_stage_id),
    stadium_id INTEGER REFERENCES stadium(stadium_id),
    match_date DATE,
    kick_off TIME,
    match_week INTEGER
);

CREATE TABLE team (
    team_id INTEGER PRIMARY KEY,
    team_name VARCHAR(50) NOT NULL
);

CREATE TABLE player_position (
    position_id INTEGER PRIMARY KEY,
    position_name VARCHAR(50) NOT NULL
);

CREATE TABLE lineup_team (
    lineup_team_id INTEGER PRIMARY KEY,
    match_id INTEGER REFERENCES game_match(match_id),
    team_id INTEGER REFERENCES team(team_id),
    score INTEGER,
    home_team BOOLEAN
);

CREATE TABLE lineup_player (
    lineup_player_id INTEGER PRIMARY KEY,
    lineup_team_id INTEGER REFERENCES lineup_team(lineup_team_id),
    player_id INTEGER REFERENCES player(player_id),
    jersey_number INTEGER
);

CREATE TABLE lineup_manager (
    lineup_manager_id INTEGER PRIMARY KEY,
    lineup_team_id INTEGER REFERENCES lineup_team(lineup_team_id),
    manager_id INTEGER REFERENCES manager(manager_id)
);

CREATE TABLE lineup_player_position (
    lineup_player_position_id INTEGER PRIMARY KEY,
    lineup_player_id INTEGER REFERENCES lineup_player(lineup_player_id),
    position_id INTEGER REFERENCES player_position(position_id),
    from_time VARCHAR(10),
    to_time VARCHAR(10),
    from_period INTEGER,
    to_period INTEGER,
    start_reason VARCHAR(50),
    end_reason VARCHAR(50)
);

CREATE TABLE penalty_card (
    card_type INTEGER PRIMARY KEY,
    card VARCHAR(15) NOT NULL
);

CREATE TABLE lineup_player_card (
    lineup_player_card_id INTEGER PRIMARY KEY,
    lineup_player_id INTEGER REFERENCES lineup_player(lineup_player_id),
    game_time VARCHAR(10),
    card_type INTEGER REFERENCES penalty_card(card_type),
    reason VARCHAR(50),
    game_period INTEGER
);

CREATE TABLE event_type (
    event_type_id INTEGER PRIMARY KEY,
    event_type_name VARCHAR(50) NOT NULL
);

CREATE TABLE play_pattern (
    play_pattern_id INTEGER PRIMARY KEY,
    play_pattern_name VARCHAR(50) NOT NULL
);

CREATE TABLE event (
    event_id INTEGER PRIMARY KEY,
    event_type_id INTEGER REFERENCES event_type(event_type_id),
    event_index INTEGER NOT NULL,
    event_period INTEGER NOT NULL,
    event_timestamp TIME NOT NULL,
    play_pattern_id INTEGER REFERENCES play_pattern(play_pattern_id),
    possession INTEGER NOT NULL
);

CREATE TABLE related_event (
    related_event_id INTEGER PRIMARY KEY,
    original_event_id INTEGER REFERENCES event(event_id),
    original_type_id INTEGER REFERENCES event_type(event_type_id),
    related_id INTEGER REFERENCES event(event_id),
    related_type_id INTEGER REFERENCES event_type(event_type_id)
);

-- Event 14: Dribble
CREATE TABLE event_14 ( 
    event_14_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    player_id INTEGER REFERENCES player(player_id),
    team_id INTEGER REFERENCES team(team_id),
    complete BOOLEAN NOT NULL
);

-- Event 16: Shot
CREATE TABLE event_16 (
    event_16_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    player_id INTEGER REFERENCES player(player_id),
    team_id INTEGER REFERENCES team(team_id),
    xg_score FLOAT NOT NULL,
    first_time BOOLEAN NOT NULL
);

-- Event 30: Pass
CREATE TABLE event_30 (
    event_30_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    player_id INTEGER REFERENCES player(player_id),
    team_id INTEGER REFERENCES team(team_id),
    recipient_id INTEGER REFERENCES player(player_id),
    through_ball BOOLEAN NOT NULL
);

-- Event 39: Dribbled Past
CREATE TABLE event_39 (
    event_39_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    player_id INTEGER REFERENCES player(player_id),
    team_id INTEGER REFERENCES team(team_id),
    event_14_id INTEGER REFERENCES event_14(event_14_id),
    completed_dribble BOOLEAN NOT NULL
);

-- Indexes for optimizing
CREATE INDEX q1_q2_index ON event_16(match_id int4_ops,player_id int4_ops);
CREATE INDEX q3_index ON event_16(first_time bool_ops,match_id int4_ops,player_id int4_ops);
CREATE INDEX q4_index ON event_30(match_id int4_ops,team_id int4_ops);
CREATE INDEX q5_index ON event_30(match_id int4_ops,recipient_id int4_ops);
CREATE INDEX q6_index ON event_16(match_id int4_ops,team_id int4_ops);
CREATE INDEX q7_index ON event_30(through_ball bool_ops,match_id int4_ops,player_id int4_ops);
CREATE INDEX q8_index ON event_30(through_ball bool_ops,match_id int4_ops,team_id int4_ops);
CREATE INDEX q9_index ON event_14(complete bool_ops,match_id int4_ops,player_id int4_ops);
CREATE INDEX q10_index ON event_39(match_id int4_ops,player_id int4_ops);

-- Experimental
/*
ALTER TABLE event_16 ADD COLUMN season_id INTEGER;
UPDATE event_16 e16 SET season_id = gm.season_id FROM game_match gm WHERE e16.match_id = gm.match_id;
CREATE INDEX ON event_16(season_id);

ALTER TABLE event_30 ADD COLUMN season_id INTEGER;
UPDATE event_30 e30 SET season_id = gm.season_id FROM game_match gm WHERE e30.match_id = gm.match_id;
CREATE INDEX ON event_30(season_id);

ALTER TABLE event_14 ADD COLUMN season_id INTEGER;
UPDATE event_14 e14 SET season_id = gm.season_id FROM game_match gm WHERE e14.match_id = gm.match_id;
CREATE INDEX ON event_14(season_id);

ALTER TABLE event_39 ADD COLUMN season_id INTEGER;
UPDATE event_39 e39 SET season_id = gm.season_id FROM game_match gm WHERE e39.match_id = gm.match_id;
CREATE INDEX ON event_39(season_id);

CREATE INDEX q1_q2_index ON event_16(season_id int4_ops,player_id int4_ops);
CREATE INDEX q3_index ON event_16(first_time bool_ops,season_id int4_ops,player_id int4_ops);
CREATE INDEX q4_index ON event_30(season_id int4_ops,team_id int4_ops);
CREATE INDEX q5_index ON event_30(season_id int4_ops,recipient_id int4_ops);
CREATE INDEX q6_index ON event_16(season_id int4_ops,team_id int4_ops);
CREATE INDEX q7_index ON event_30(through_ball bool_ops,season_id int4_ops,player_id int4_ops);
CREATE INDEX q8_index ON event_30(through_ball bool_ops,season_id int4_ops,team_id int4_ops);
CREATE INDEX q9_index ON event_14(complete bool_ops,season_id int4_ops,player_id int4_ops);
CREATE INDEX q10_index ON event_39(season_id int4_ops,player_id int4_ops);
*/

/* Various types */

CREATE TABLE outcome (
    outcome_id INTEGER PRIMARY KEY,
    outcome_name VARCHAR(50) NOT NULL
);

CREATE TABLE body_part (
    body_part_id INTEGER PRIMARY KEY,
    body_part_name VARCHAR(50) NOT NULL
);

CREATE TABLE duel_type (
    duel_type_id INTEGER PRIMARY KEY,
    duel_type_name VARCHAR(50) NOT NULL
);

CREATE TABLE foul_type (
    foul_type_id INTEGER PRIMARY KEY,
    foul_type_name VARCHAR(50) NOT NULL
);

CREATE TABLE shot_type (
    shot_type_id INTEGER PRIMARY KEY,
    shot_type_name VARCHAR(50) NOT NULL
);

CREATE TABLE pass_type (
    pass_type_id INTEGER PRIMARY KEY,
    pass_type_name VARCHAR(50) NOT NULL
);

CREATE TABLE shot_technique (
    shot_technique_id INTEGER PRIMARY KEY,
    shot_technique_name VARCHAR(50) NOT NULL
);

CREATE TABLE pass_technique (
    pass_technique_id INTEGER PRIMARY KEY,
    pass_technique_name VARCHAR(50) NOT NULL
);

-- Event 14 Metadata
CREATE TABLE event_14_metadata (
    event_14_metadata_id SERIAL PRIMARY KEY,
    event_14_id INTEGER REFERENCES event_14(event_14_id),
    location_x FLOAT,
    location_y FLOAT,
    duration FLOAT
);

-- Event 16 Metadata
CREATE TABLE event_16_metadata (
    event_16_metadata_id SERIAL PRIMARY KEY,
    event_16_id INTEGER REFERENCES event_16(event_16_id),
    location_x FLOAT,
    location_y FLOAT,
    duration FLOAT,
    shot_type_id INTEGER REFERENCES shot_type(shot_type_id),
    outcome_id INTEGER REFERENCES outcome(outcome_id),
    shot_technique_id INTEGER REFERENCES shot_technique(shot_technique_id),
    body_part_id INTEGER REFERENCES body_part(body_part_id),
    end_location_x FLOAT,
    end_location_y FLOAT,
    deflected BOOLEAN,
    one_on_one BOOLEAN,
    aerial_won BOOLEAN,
    saved_to_post BOOLEAN,
    redirect BOOLEAN,
    open_goal BOOLEAN,
    follows_dribble BOOLEAN,
    saved_off_target BOOLEAN
);

-- Event 30 Metadata
CREATE TABLE event_30_metadata (
    event_30_metadata_id SERIAL PRIMARY KEY,
    event_30_id INTEGER REFERENCES event_30(event_30_id),
    location_x FLOAT,
    location_y FLOAT,
    duration FLOAT,
    length FLOAT,
    angle FLOAT,
    pass_type_id INTEGER REFERENCES pass_type(pass_type_id),
    outcome_id INTEGER REFERENCES outcome(outcome_id),
    pass_technique_id INTEGER REFERENCES pass_technique(pass_technique_id),
    body_part_id INTEGER REFERENCES body_part(body_part_id),
    end_location_x FLOAT,
    end_location_y FLOAT,
    aerial_won BOOLEAN,
    shot_assist BOOLEAN,
    pass_switch BOOLEAN,
    pass_cross BOOLEAN,
    deflected BOOLEAN,
    inswinging BOOLEAN,
    through_ball BOOLEAN,
    no_touch BOOLEAN,
    outswinging BOOLEAN,
    miscommunication BOOLEAN,
    cut_back BOOLEAN,
    goal_assist BOOLEAN,
    straight BOOLEAN
);

-- Event 39 Metadata
CREATE TABLE event_39_metadata (
    event_39_metadata_id SERIAL PRIMARY KEY,
    event_39_id INTEGER REFERENCES event_39(event_39_id),
    location_x FLOAT,
    location_y FLOAT,
    duration FLOAT
);

/* Additional Events */

-- Event 02 : Ball Recovery
CREATE TABLE event_02 (
    event_02_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    player_id INTEGER REFERENCES player(player_id),
    team_id INTEGER REFERENCES team(team_id),
    location_x FLOAT,
    location_y FLOAT,
    duration FLOAT
);

-- Event 03 : Dispossessed
CREATE TABLE event_03 (
    event_03_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    player_id INTEGER REFERENCES player(player_id),
    team_id INTEGER REFERENCES team(team_id),
    location_x FLOAT,
    location_y FLOAT,
    duration FLOAT
);

-- Event 04 : Duel
CREATE TABLE event_04 (
    event_04_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    player_id INTEGER REFERENCES player(player_id),
    team_id INTEGER REFERENCES team(team_id),
    location_x FLOAT,
    location_y FLOAT,
    duration FLOAT,
    duel_type_id INTEGER REFERENCES duel_type(duel_type_id),
    outcome_id INTEGER REFERENCES outcome(outcome_id)
);

-- Event 05 : Camera On
CREATE TABLE event_05 (
    event_05_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    player_id INTEGER REFERENCES player(player_id),
    team_id INTEGER REFERENCES team(team_id)
);

-- Event 06 : Block
CREATE TABLE event_06 (
    event_06_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    player_id INTEGER REFERENCES player(player_id),
    team_id INTEGER REFERENCES team(team_id),
    location_x FLOAT,
    location_y FLOAT,
    duration FLOAT,
    deflection BOOLEAN,
    offensive BOOLEAN,
    save_block BOOLEAN
);

-- Event 08 : Offside
CREATE TABLE event_08 (
    event_08_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    player_id INTEGER REFERENCES player(player_id),
    team_id INTEGER REFERENCES team(team_id),
    location_x FLOAT,
    location_y FLOAT,
    duration FLOAT
);

-- Event 09 : Clearance
CREATE TABLE event_09 (
    event_09_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    player_id INTEGER REFERENCES player(player_id),
    team_id INTEGER REFERENCES team(team_id),
    location_x FLOAT,
    location_y FLOAT,
    duration FLOAT,
    aerial_won BOOLEAN,
    body_part_id INTEGER REFERENCES body_part(body_part_id)
);

-- Event 10 : Interception
CREATE TABLE event_10 (
    event_10_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    player_id INTEGER REFERENCES player(player_id),
    team_id INTEGER REFERENCES team(team_id),
    location_x FLOAT,
    location_y FLOAT,
    duration FLOAT,
    outcome_id INTEGER REFERENCES outcome(outcome_id)
);

-- Event 17 : Pressure
CREATE TABLE event_17 (
    event_17_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    player_id INTEGER REFERENCES player(player_id),
    team_id INTEGER REFERENCES team(team_id),
    location_x FLOAT,
    location_y FLOAT,
    duration FLOAT,
    counterpress BOOLEAN
);

-- Event 18 : Half Start
CREATE TABLE event_18 (
    event_18_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    duration FLOAT,
    late_video_start BOOLEAN
);

-- Event 19 : Substitution
CREATE TABLE event_19 (
    event_19_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    player_id INTEGER REFERENCES player(player_id),
    team_id INTEGER REFERENCES team(team_id),
    duration FLOAT,
    outcome_id INTEGER,
    replacement_id INTEGER REFERENCES player(player_id)
);

-- Event 20 : Own Goal Against
CREATE TABLE event_20 (
    event_20_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    player_id INTEGER REFERENCES player(player_id),
    team_id INTEGER REFERENCES team(team_id),
    location_x FLOAT,
    location_y FLOAT,
    duration FLOAT
);

-- Event 21 : Foul Won
CREATE TABLE event_21 (
    event_21_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    player_id INTEGER REFERENCES player(player_id),
    team_id INTEGER REFERENCES team(team_id),
    location_x FLOAT,
    location_y FLOAT,
    duration FLOAT,
    penalty BOOLEAN,
    defensive BOOLEAN,
    advantage BOOLEAN
);

-- Event 22 : Foul Committed
CREATE TABLE event_22 (
    event_22_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    player_id INTEGER REFERENCES player(player_id),
    team_id INTEGER REFERENCES team(team_id),
    location_x FLOAT,
    location_y FLOAT,
    duration FLOAT,
    penalty BOOLEAN,
    advantage BOOLEAN,
    offensive BOOLEAN,
    penalty_card_id INTEGER REFERENCES penalty_card(card_type),
    foul_id INTEGER REFERENCES foul_type(foul_type_id)
);

-- Event 23 : Goal Keeper #@@
CREATE TABLE event_23 (
    event_23_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    player_id INTEGER REFERENCES player(player_id),
    team_id INTEGER REFERENCES team(team_id),
    location_x FLOAT,
    location_y FLOAT,
    duration FLOAT
);

-- Event 24 : Bad Behaviour
CREATE TABLE event_24 (
    event_24_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    player_id INTEGER REFERENCES player(player_id),
    team_id INTEGER REFERENCES team(team_id),
    duration FLOAT,
    penalty_card_id INTEGER REFERENCES penalty_card(card_type)
);

-- Event 25 : Own Goal For
CREATE TABLE event_25 (
    event_25_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    player_id INTEGER REFERENCES player(player_id),
    team_id INTEGER REFERENCES team(team_id),
    location_x FLOAT,
    location_y FLOAT,
    duration FLOAT
);

-- Event 26 : Player On
CREATE TABLE event_26 (
    event_26_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    player_id INTEGER REFERENCES player(player_id),
    team_id INTEGER REFERENCES team(team_id),
    location_x FLOAT,
    location_y FLOAT,
    duration FLOAT
);

-- Event 27 : Player Off
CREATE TABLE event_27 (
    event_27_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    player_id INTEGER REFERENCES player(player_id),
    team_id INTEGER REFERENCES team(team_id),
    location_x FLOAT,
    location_y FLOAT,
    duration FLOAT
);

-- Event 28 : Shield
CREATE TABLE event_28 (
    event_28_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    player_id INTEGER REFERENCES player(player_id),
    team_id INTEGER REFERENCES team(team_id),
    location_x FLOAT,
    location_y FLOAT,
    duration FLOAT
);

-- Event 29 : Camera off
CREATE TABLE event_29 (
    event_29_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    player_id INTEGER REFERENCES player(player_id),
    team_id INTEGER REFERENCES team(team_id),
    location_x FLOAT,
    location_y FLOAT,
    duration FLOAT
);

-- Event 33 : 50/50
CREATE TABLE event_33 (
    event_33_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    player_id INTEGER REFERENCES player(player_id),
    team_id INTEGER REFERENCES team(team_id),
    location_x FLOAT,
    location_y FLOAT,
    duration FLOAT,
    outcome_id INTEGER REFERENCES outcome(outcome_id)
);

-- Event 34 : Half End
CREATE TABLE event_34 (
    event_34_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    team_id INTEGER REFERENCES team(team_id),
    duration FLOAT
);

-- Event 35 : Starting XI #@@
CREATE TABLE event_35 (
    event_35_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    team_id INTEGER REFERENCES team(team_id),
    duration FLOAT
);

-- Event 36 : Tactical Shift #@@
CREATE TABLE event_36 (
    event_36_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    team_id INTEGER REFERENCES team(team_id),
    duration FLOAT
);

-- Event 37 : Error
CREATE TABLE event_37 (
    event_37_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    player_id INTEGER REFERENCES player(player_id),
    team_id INTEGER REFERENCES team(team_id),
    location_x FLOAT,
    location_y FLOAT,
    duration FLOAT
);

-- Event 38 : Miscontrol
CREATE TABLE event_38 (
    event_38_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    player_id INTEGER REFERENCES player(player_id),
    team_id INTEGER REFERENCES team(team_id),
    location_x FLOAT,
    location_y FLOAT,
    duration FLOAT,
    aerial_won BOOLEAN
);

-- Event 40 : Injury Stoppage
CREATE TABLE event_40 (
    event_40_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    player_id INTEGER REFERENCES player(player_id),
    team_id INTEGER REFERENCES team(team_id),
    location_x FLOAT,
    location_y FLOAT,
    duration FLOAT,
    in_chain BOOLEAN
);

-- Event 41 : Referee Ball-Drop
CREATE TABLE event_41 (
    event_41_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    team_id INTEGER REFERENCES team(team_id),
    location_x FLOAT,
    location_y FLOAT,
    duration FLOAT
);

-- Event 42 : Ball Receipt*
CREATE TABLE event_42 (
    event_42_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    player_id INTEGER REFERENCES player(player_id),
    team_id INTEGER REFERENCES team(team_id),
    location_x FLOAT,
    location_y FLOAT,
    outcome_id INTEGER REFERENCES outcome(outcome_id)
);

-- Event 43 : Carry
CREATE TABLE event_43 (
    event_43_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    player_id INTEGER REFERENCES player(player_id),
    team_id INTEGER REFERENCES team(team_id),
    location_x FLOAT,
    location_y FLOAT,
    end_location_x FLOAT,
    end_location_y FLOAT,
    duration FLOAT
);