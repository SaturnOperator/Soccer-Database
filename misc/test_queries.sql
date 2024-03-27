-- Get Argentinian players
SELECT player_name, country_name
FROM player
INNER JOIN country ON player.country_id = country.country_id
WHERE country_name = 'Argentina';

-- Get number of home and away games played by each team
SELECT team.team_name, COUNT(CASE WHEN lineup_team.home_team THEN 1 END) AS home_games, COUNT(CASE WHEN NOT lineup_team.home_team THEN 1 END) AS away_games
FROM team
INNER JOIN lineup_team ON team.team_id = lineup_team.team_id
GROUP BY team.team_name;

-- Get number matches played by each spanish player during season
SELECT 
    p.player_name,
    pp.position_name,
    COUNT(DISTINCT gm.match_id) AS num_matches_played
FROM player AS p
JOIN country AS c ON p.country_id = c.country_id
JOIN lineup_player AS lp ON p.player_id = lp.player_id
JOIN lineup_team AS lt ON lp.lineup_team_id = lt.lineup_team_id
JOIN game_match AS gm ON lt.match_id = gm.match_id
JOIN season AS s ON gm.season_id = s.season_id
JOIN competition AS comp ON s.competition_id = comp.competition_id
JOIN lineup_player_position AS lpp ON lp.lineup_player_id = lpp.lineup_player_id
JOIN player_position AS pp ON lpp.position_id = pp.position_id
WHERE 
    c.country_name = 'Spain' 
    AND comp.competition_name = 'La Liga' 
    AND s.season_name = '2020/2021'
GROUP BY p.player_name, pp.position_name
ORDER BY num_matches_played DESC;


-- Get number of yellow cards of each player 
SELECT 
    p.player_name,
    COUNT(*) AS cards_received
FROM player AS p
JOIN lineup_player AS lp ON p.player_id = lp.player_id
JOIN lineup_player_card AS lpc ON lp.lineup_player_id = lpc.lineup_player_id
JOIN penalty_card AS pc ON lpc.card_type = pc.card_type
JOIN lineup_team AS lt ON lp.lineup_team_id = lt.lineup_team_id
JOIN game_match AS gm ON lt.match_id = gm.match_id
JOIN season AS s ON gm.season_id = s.season_id
JOIN competition AS comp ON s.competition_id = comp.competition_id
WHERE 
    pc.card = 'Yellow Card'
    AND comp.competition_name = 'La Liga' 
    AND s.season_name = '2020/2021'
GROUP BY p.player_name
HAVING COUNT(*) > 1
ORDER BY cards_received DESC;