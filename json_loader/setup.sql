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
    season_id INTEGER NOT NULL,
    country_id INTEGER REFERENCES country(country_id),
    competition_name VARCHAR(50) NOT NULL,
    season_name VARCHAR(50) NOT NULL,
    competition_gender VARCHAR(10),
    competition_youth BOOLEAN,
    competition_international BOOLEAN
);

CREATE TABLE game_match (
    match_id INTEGER PRIMARY KEY,
    competition_id INTEGER REFERENCES competition(competition_id),
    season_id INTEGER NOT NULL,
    match_date DATE,
    kick_off TIME,
    match_week INTEGER,
    competition_stage_id INTEGER REFERENCES competition_stage(competition_stage_id),
    stadium_id INTEGER REFERENCES stadium(stadium_id)
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
    manager_id INTEGER REFERENCES manager(manager_id),
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

-- Indexes for the player table
CREATE INDEX idx_player_country ON player(country_id);

-- Indexes for the competition table
CREATE INDEX idx_competition_season_country ON competition(season_id, country_id);
CREATE INDEX idx_competition_id ON competition(competition_id);

-- Indexes for the game_match table
CREATE INDEX idx_game_match_competition_season ON game_match(competition_id, season_id);
CREATE INDEX idx_game_match_id ON game_match(match_id);

-- Indexes for the lineup_team table
CREATE INDEX idx_lineup_team_match_team ON lineup_team(match_id, team_id);

-- Indexes for the lineup_player table
CREATE INDEX idx_lineup_player_lineup_team_player ON lineup_player(lineup_team_id, player_id);

-- Indexes for the lineup_player_position table
CREATE INDEX idx_lineup_player_position_lineup_player_position ON lineup_player_position(lineup_player_id, position_id);
