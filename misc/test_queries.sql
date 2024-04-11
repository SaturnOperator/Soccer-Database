-- Q1
SELECT p.player_name, AVG(e16.xg_score) AS avg_xg_score
FROM player p
JOIN event_16 e16 ON p.player_id = e16.player_id
JOIN game_match m ON e16.match_id = m.match_id
JOIN season s ON m.season_id = s.season_id
WHERE s.season_name = '2020/2021' AND e16.xg_score IS NOT NULL
GROUP BY p.player_name
ORDER BY avg_xg_score DESC;

SELECT p.player_name, AVG(e16.xg_score) AS avg_xg_score
FROM event_16 e16
JOIN player p ON e16.player_id = p.player_id
JOIN game_match m ON e16.match_id = m.match_id
JOIN season s ON m.season_id = s.season_id
WHERE s.season_name = '2020/2021' AND e16.xg_score IS NOT NULL
GROUP BY p.player_name
ORDER BY avg_xg_score DESC;


-- Q2
SELECT p.player_name, COUNT(e16.event_id) AS shots_count
FROM player p
JOIN event_16 e16 ON p.player_id = e16.player_id
JOIN game_match m ON e16.match_id = m.match_id
JOIN season s ON m.season_id = s.season_id
WHERE s.season_name = '2020/2021'
GROUP BY p.player_name
ORDER BY shots_count DESC;

-- Q3
SELECT p.player_name, COUNT(e16.event_id) AS first_time_shots
FROM player p
JOIN event_16 e16 ON p.player_id = e16.player_id
JOIN game_match m ON e16.match_id = m.match_id
JOIN season s ON m.season_id = s.season_id
WHERE s.season_name IN ('2020/2021', '2019/2020', '2018/2019') AND e16.first_time = TRUE
GROUP BY p.player_name
ORDER BY first_time_shots DESC;

-- Q4
SELECT t.team_name, COUNT(e30.event_id) AS passes_count
FROM team t
JOIN event_30 e30 ON t.team_id = e30.team_id
JOIN game_match m ON e30.match_id = m.match_id
JOIN season s ON m.season_id = s.season_id
WHERE s.season_name = '2020/2021'
GROUP BY t.team_name
ORDER BY passes_count DESC;

-- Q5
SELECT p.player_name, COUNT(e30.recipient_id) AS recipient_count
FROM player p
JOIN event_30 e30 ON p.player_id = e30.recipient_id
JOIN game_match m ON e30.match_id = m.match_id
JOIN season s ON m.season_id = s.season_id
WHERE s.season_name = '2003/2004'
GROUP BY p.player_name
ORDER BY recipient_count DESC;

-- Q6
SELECT t.team_name, COUNT(e16.event_id) AS shots_count
FROM team t
JOIN event_16 e16 ON t.team_id = e16.team_id
JOIN game_match m ON e16.match_id = m.match_id
JOIN season s ON m.season_id = s.season_id
WHERE s.season_name = '2003/2004'
GROUP BY t.team_name
ORDER BY shots_count DESC;

-- Q7
SELECT p.player_name, COUNT(e30.event_id) AS through_balls_count
FROM event_30 e30
JOIN game_match m ON e30.match_id = m.match_id
JOIN season s ON m.season_id = s.season_id
JOIN player p ON e30.player_id = p.player_id 
WHERE s.season_name = '2020/2021' AND e30.through_ball = True
GROUP BY p.player_name
ORDER BY through_balls_count DESC;

-- Q8
SELECT t.team_name, COUNT(e30.event_id) AS through_balls_count
FROM event_30 e30
JOIN game_match m ON e30.match_id = m.match_id
JOIN season s ON m.season_id = s.season_id
JOIN team t ON e30.team_id = t.team_id
WHERE s.season_name = '2020/2021' AND e30.through_ball = True
GROUP BY t.team_name
ORDER BY through_balls_count DESC;

-- Q9 
SELECT p.player_name, COUNT(e14.event_id) AS completed_dribbles
FROM player p
JOIN event_14 e14 ON p.player_id = e14.player_id
JOIN game_match m ON e14.match_id = m.match_id
JOIN season s ON m.season_id = s.season_id
WHERE s.season_name IN ('2020/2021', '2019/2020', '2018/2019') AND e14.complete = TRUE
GROUP BY p.player_name
ORDER BY completed_dribbles DESC;

-- Q10
SELECT p.player_name, COUNT(e39.event_id) AS dribbled_past
FROM player p
JOIN event_39 e39 ON p.player_id = e39.player_id
JOIN game_match m ON e39.match_id = m.match_id
JOIN season s ON m.season_id = s.season_id
WHERE s.season_name = '2020/2021'
GROUP BY p.player_name
ORDER BY dribbled_past ASC;