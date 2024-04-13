# Soccer Database

```
Abdullah Mostafa
101008311
COMP 3005
```

## Conceptual Design

The schema can be broken down into 3 different aspects:

1.  **Key entities**: These are tables that store general data that are used and referenced throughout the rest of the database such as Teams, Players, Countries, Season, Matches etc.
2.  **Events data tables**: These tables contain the necessary data needed to conduct queries. For example table `event_16` which contains Shot events data.
3.  **Events metadata tables**: These tables contain auxiliary to the events data table, these contain information that isn't always needed in the usual queries but is ready and accessible when needed. The events data is split up into these two categories to optimize for lookup efficiency. For example: `event_16_metadata` contains additional info to each event in `event_16` table and can be looked up through a FK pointing to the `event_16_id`.



Soccer teams can be very dynamic, in one season a player x can be team A, and in the next can be on team B. Alternatively the same player can play different positions and have different jersey numbers across different matches. By this nature you cannot tie a player to a team, nor give him a fixed position or jersey number. To combat this, the `player` table only contains fixed info on a player such as their name and their nationality and an id. Likewise the `team` table only has a team name and a team id. A set of intermediary tables starting with the name `lineup_*` links players to teams and teams to matches. These `lineup_*` tables hold match specific information on a team, player etc. For example `lineup_team` holds the team's score, and if they're the home team. The `lineup_player` hold the jersey number and is associated to a `lineup_team` which can retrieve the team's line up for that match. Moreover `lineup_player_poisiton`  is associated to a `lineup_player`, a player can have multiple positions throughout a match and each entry in this table reflects that. This is a simplified subset of the ER diagram of how the game-team-player associations work:

```mermaid
erDiagram
    game_match ||--o{ lineup_team : ""
    lineup_team ||--o{ lineup_player : ""
    lineup_player ||--o{ lineup_player_position : ""
    
    team ||--|| lineup_team : "FK: team_id"
    player ||--|| lineup_player : "FK: player_id"
    player_position ||--|| lineup_player_position : "FK: player_position_id"
```



The event table design is broken into 3 aspects, there is one main table `event` that contains all the events. This table holds general attributes shared across each event such as the type of event, timestamp, play style etc. There is a `related_event` table which holds record of an event's related event ids, if an event has multiple then there will be multiple entries (one for each related event). Each specific event type is broken out into their own specific tables, this is done this way as different event types have different attributes, this also significantly speeds up query times when you are only interested in one event type. Some event (events 14, 16, 30 and 39) have an auxiliary table called `event_#_metadata` which is associated to its respective `event_#` table through a FK, this is done to increase query efficiency as the tables for events 14, 16, 30 and 39 only store the necessary information for the queries, meanwhile their respective auxiliary tables contain the rest of the data of the event.

```mermaid
erDiagram

		event }o--o{ related_event : "FK: event_id"
    event ||--o{ event_14 : "FK: event_id"
    event_14 ||--|| event_14_metadata : "event_14_id"
    game_match ||--o{ event_14 : "FK :match_id"
		
```





### Cardinalities:

1. One to many: `country`, `stadium`, `competition`,`season`, `game_match`, `team_lineup`, `player_position`, `event_type`, `play_pattern`, `events` etc.. are all one to many as entities that contain these will only contain one. For example a stadium can only have 1 country, a match can only have 1 season, a season can only have 1 competition,  and so on.
1. Many to many: `team`, `player`, `manager`, `related_event` etc, these entities are many to many as many teams can have many players, etc

## Relation Schemas

- **country**: 
  - `country_id` (PK), `country_name`
- **player**: Player, their country and nicknames
  - `player_id` (PK), `player_name`, `player_nickname`, `country_id` (FK)
- **manager**: Managers
  - `manager_id` (PK), `manager_name`, `manager_nickname`, `dob`, `country_id `(FK)
- **stadium**: Stadium name and country
  - `stadium_id` (PK), `stadium_name`, `country_id` (FK)
- **competition_stage**: 
  - `competition_stage_id` (FK), `competition_stage_name`
- **competition**: 
  - `competition_id` (PK), `competition_name`, `location`, `gender`, `youth`, `international`
- **season**: season data, associated to a competition through FK
  - `season_id` (PK), `season_name`, `competition_id` (FK)
- **game_match**: match data, associated to a season through FK
  - `match_id` (PK), `season_id` (FK), `competition_stage_id` (FK), `stadium_id` (FK), `match_date`, `kick_off`, `match_week`
- **team**: 
  - `team_id` (PK), `team_name`
- **player_position**: 
  - `position_id` (PK), `position_name`
- **lineup_team**: Associated to a **game_match**. Each match has two teams, **lineup_team** stores what the team scored that game and if that team is the home team. A **lineup_team** is associated to a team through the `team_id` FK, this is done this way as different teams can yield different scores, teams can also vary between being home team and away team in different matches, thus this intermediate table links a team along with a match. A lineup_team entry is just a name, the **lineup_team** is what contains all the players for that game.
  - `lineup_team_id` (PK), `match_id` (FK), `team_id` (FK), `score`, `home_team`
- **lineup_player**: Associated to a `lineup_team`, this is done this way as teams can have different players each match, the same player could have different jersey number across different match etc. This intermediate table lets us map 
  - `lineup_player_id` (PK), `lineup_team_id` (FK), `player_id` (FK), `jersey_number`
- **lineup_player_position**: 
  - `lineup_player_position_id` (PK), `lineup_player_id` (FK), `position_id` (FK), `from_time`, `to_time`, `from_period`, `to_period`, `start_reason`, `end_reason`
- **lineup_manager**: Similar to how a **lineup_player** is linked to a **lineup_team_id** which is linked to a **game_match**.
    - `lineup_manager_id` (PK), `lineup_team_id` (FK), `manager_id` (FK)
- **penalty_card**: 
  - `card_type` (PK), `card`
- **lineup_player_card**: Associated to a **lineup_player** and explains when and why they got the card
  - `lineup_player_card_id` (PK), `lineup_player_id` (FK), `game_time`, `card_type` (FK), `reason`, `game_period`
- **event_type**: 
  - `event_type_id` (PK), `event_type_name`
- **play_pattern**: 
  - `play_pattern_id` (PK), `play_pattern_name`
- **pass_type**: 
  - `pass_type_id` (PK), `pass_type_name`
- **event**: Stores basic info on every event
  - `event_id` (PK), `event_type_id` (FK), `event_index`, `event_period`, `event_timestamp`, `play_pattern_id` (FK), `possession`
- **related_event**: You can find an event's related events in this table
  - `related_event_id` (PK), `original_event_id` (FK), `original_type_id` (FK), `related_id` (FK), `related_type_id` (FK)
- **event_14**: Dribble event
  - `event_14_id` (PK), `event_id` (FK), `match_id` (FK), `player_id` (FK), `team_id` (FK), `complete`
- **event_16**: Shot event
  - ``event_16_id` (PK), `event_id` (FK), `match_id` (FK), `player_id` (FK), `team_id` (FK), `xg_score`, `first_time``
- **event_30**: Pass event
  - `event_30_id` (PK), `event_id` (FK), `match_id` (FK), `player_id` (FK), `team_id` (FK), `recipient_id` (FK), `through_ball`
- **event_39**: Dribbled Past event
  - `event_39_id` (PK), `event_id` (FK), `match_id` (FK), `player_id` (FK), `team_id` (FK), `event_14_id` (FK), `completed_dribble`

### 

## Database Schema Diagram

```mermaid
erDiagram
	country {
		int country_id PK
		string country_name
	}
	
	competition {
		int competition_id PK
		string competition_name
		string competition_location
		string competition_gender
		bool competition_youth
		bool competition_international
	}
	
	season {
			int season_id
			string season_name
			int competition_id FK
	}
	
	stadium {
			int stadium_id PK
			int country_id FK
			string stadium_name
	}
	
	manager {
			int manager_id PK
			int country_id FK
			string manager_name
			string manager_nickname
			string dob
	}
	
	competition_stage {
			int competition_stage_id FK
			string competition_stage_name
	}
	
	game_match {
			int match_id PK
			int season_id FK
				string match_date
				string kick_off
				int match_week
				int competition_stage_id FK
				int stadium_id FK
	}
   
	
	team {
			int team_id PK
			string team_name
	}
	
	player_position {
			int position_id PK
			string position_name
	}
	
	lineup_team {
			int lineup_team_id PK
			int match_id FK
			int team_id FK
			int score
			bool home_team
	}
	
	lineup_player {
		int lineup_player_id PK
		int lineup_team_id FK
		int player_id FK
		int jersey_number
	}
	
	lineup_manager {
		int lineup_manager_id PK
		int lineup_team_id FK
		int manager_id FK
	}
	
	lineup_player_position {
			int lineup_player_position_id PK
			int lineup_player_id FK
			int position_id FK
			string from_time
			string to_time
			int from_period
			int to_period
			string start_reason
			string end_reason
	}
	
	penalty_card {
			int card_type PK
			string card
	}
	
	lineup_player_card {
			int lineup_player_card_id PK
			int lineup_player_id FK
			string game_time
			int card_type FK
			string reason
			int game_period
	}
	
	player {
			int player_id PK
			int country_id
			string player_name
			string player_nickname
	}
	
	
	lineup_team ||--|| lineup_manager : "FK: lineup_team_id"
	team ||--|| lineup_team : "FK: team_id"
	lineup_team ||--|| lineup_player : "FK: lineup_team_id"
	country ||--|| competition : "FK: country_id"
	competition ||--|| season : "FK: competition_id"
	season ||--|| game_match : "FK: season_id"
	stadium  ||--|| game_match : "FK: stadium_id"
	competition_stage  ||--|| game_match : "FK: competition_stage_id"
  manager  ||--|| lineup_manager : "FK: manager_id"
	game_match ||--|| lineup_team : "FK: match_id" 
	lineup_player ||--||	lineup_player_position : "FK: lineup_player_id"
	player_position ||--|| lineup_player_position : "FK position_id"
	lineup_player ||--||	lineup_player_card : "FK: lineup_player_id"
	penalty_card ||--|| lineup_player_card : "FK: card_type"
	player ||--||	lineup_player : "FK: player_id"
	country ||--||	player : "FK: country_id"
	
```

### Event Tables

```mermaid
%% Tables for events
	erDiagram
	event_type {
		int event_type_id
		string event_type_name
	}
	
	play_pattern {
		int play_pattern_id
		int play_pattern_name
	}
	
	event { 
		int event_id
		int event_type_id FK
		int index
		int event_period
		str event_timestamp
		int play_pattern_id FK
		int possesion
	}
	
	related_event {
		int related_event_id
		int original_event_id
		int original_type_id
		int related_id
		int related_type_id
	}
	
	body_part{
		int body_part_id
		string body_part_name
	}
	
	body_part ||--|| event_14_metadata : "FK: body_part_id"
	
	%% Event 14: Dribble
	event_14 ["event_14: Dribble"]{
		int event_14_id
		int event_id FK
		int match_id FK
		int player_id FK
		int team_id FK
		boolean complete
	}
	
	event_14_metadata {
		int event_14_metadata_id
		int event_14_id FK
		float location_x
		float location_y
		float duration
		bool under_pressure
	}
	
	%% Event 16: Shot
	event_16 ["event_16: Shot"]{
		int event_16_id
		int event_id FK
		int match_id FK
		int player_id FK
		int team_id FK
		float xg_score
		bool first
	}
	
	event_16_metadata {
		int event_16_metadata_id
		int event_16_id FK
		float location_x
		float location_y
		float location_z
		float duration
		int shot_technique_id FK
		int body_part_id FK
		int shot_type_id FK
		int shot_outcome_id FK
	}
	
	shot_type {
		int shot_type_id
		string shot_type_name
	}
	
	shot_technique {
		int shot_technique_id
		string shot_technique_name
	}
	
	shot_outcome {
		int shot_outcome_id
		string shot_outcome_name
	}
	body_part ||--|| event_16_metadata : "FK: body_part_id"
	shot_type ||--|| event_16 : "FK: shot_type_id"
	shot_technique ||--|| event_16 : "FK: shot_technique_id"
	shot_outcome ||--|| event_16 : "FK: shot_outcome_id"
	
	%% Event 30: Pass
	event_30 ["event_30: Pass"]{
		int event_30_id
		int event_id FK
		int match_id FK
		int player_id FK
		int team_id FK
		int recipient_id FK
		bool through_ball
	}
	
	event_30_metadata {
		int event_30_metadata_id
		int event_30_id FK
		float start_location_x
		float start_location_y
		float end_location_x
		float end_location_y
		int body_part_id FK
		float pass_length
		float pass_angle
		float duration
		int pass_type_id FK
	}
	
	pass_type {
		int pass_type_id
		string pass_type_name
	}
	
	body_part ||--|| event_30_metadata : "FK: body_part_id"
	pass_type ||--|| event_30 : "FK: pass_type_id"
	
	%% Event 39: Dribbled Past
	event_39 ["event_39: Dribbled Past"]{
		int event_39_id
		int event_id FK
		int match_id FK
		int player_id FK
		int team_id FK
		int event_14_id FK
	}
	
	event_39_metadata {
		int event_39_metadata_id
		int event_39_id FK
		float location_x
		float location_y
		float duration
	}
	
	event_type ||--|| event : "FK: event_type_id"
	play_pattern ||--|| event : "FK: play_pattern_id"
	event ||--|| related_event : "FK: play_pattern_id"
	
	event_14 ||--|| event_14_metadata : "FK: event_16_id"
	event_16 ||--|| event_16_metadata : "FK: event_16_id"
	event_30 ||--|| event_30_metadata : "FK: event_30_id"
	event_39 ||--|| event_39_metadata : "FK: event_39_id"

	%%event_14 ||--|| event_39 : "FK: event_id"
	

	event ||--|| event_14 : "FK: event_id"
	event ||--|| event_16 : "FK: event_id"
	event ||--|| event_30 : "FK: event_id"
	event ||--|| event_39 : "FK: event_id"
	
	
	
	
```

