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

-- -- Indexes for the player table
-- CREATE INDEX idx_player_country ON player(country_id);

-- -- Indexes for the competition table
-- CREATE INDEX idx_competition ON competition(competition_id);

-- -- Indexes for the season table
-- CREATE INDEX idx_season_competition ON season(competition_id);
-- CREATE INDEX idx_season_id ON season(season_id);

-- -- Indexes for the game_match table
-- CREATE INDEX idx_game_match_season ON game_match(season_id);
-- CREATE INDEX idx_game_match_competition_stage ON game_match(competition_stage_id);
-- CREATE INDEX idx_game_match_stadium ON game_match(stadium_id);
-- CREATE INDEX idx_game_match_date ON game_match(match_date);

-- -- Indexes for the lineup_team table
-- CREATE INDEX idx_lineup_team_match ON lineup_team(match_id);
-- CREATE INDEX idx_lineup_team_team ON lineup_team(team_id);

-- -- Indexes for the lineup_player table
-- CREATE INDEX idx_lineup_player_lineup_team ON lineup_player(lineup_team_id);
-- CREATE INDEX idx_lineup_player_player ON lineup_player(player_id);

-- -- Indexes for the lineup_manager table
-- CREATE INDEX idx_lineup_manager_lineup_team ON lineup_manager(lineup_team_id);
-- CREATE INDEX idx_lineup_manager_manager ON lineup_manager(manager_id);

-- -- Indexes for the lineup_player_position table
-- CREATE INDEX idx_lineup_player_position_lineup_player ON lineup_player_position(lineup_player_id);
-- CREATE INDEX idx_lineup_player_position_position ON lineup_player_position(position_id);

-- -- Indexes for the lineup_player_card table
-- CREATE INDEX idx_lineup_player_card_lineup_player ON lineup_player_card(lineup_player_id);
-- CREATE INDEX idx_lineup_player_card_card_type ON lineup_player_card(card_type);

CREATE TABLE event_type (
    event_type_id INTEGER PRIMARY KEY,
    event_type_name VARCHAR(50) NOT NULL
);

CREATE TABLE play_pattern (
    play_pattern_id INTEGER PRIMARY KEY,
    play_pattern_name VARCHAR(50) NOT NULL
);

CREATE TABLE pass_type (
    pass_type_id INTEGER PRIMARY KEY,
    pass_type_name VARCHAR(50) NOT NULL
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
    xg_score FLOAT NOT NULL
);

-- Event 30: Pass
CREATE TABLE event_30 (
    event_30_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    player_id INTEGER REFERENCES player(player_id),
    team_id INTEGER REFERENCES team(team_id),
    recipient_id INTEGER REFERENCES player(player_id),
    pass_type_id INTEGER REFERENCES pass_type(pass_type_id)
);

-- Event 39: Dribbled Past
CREATE TABLE event_39 (
    event_39_id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    match_id INTEGER REFERENCES game_match(match_id),
    player_id INTEGER REFERENCES player(player_id),
    team_id INTEGER REFERENCES team(team_id),
    event_14_id INTEGER REFERENCES event_14(event_14_id)
);