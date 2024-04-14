-- Q1
SELECT p.player_name, AVG(e16.xg_score) AS avg_xg_score
FROM player p
JOIN event_16 e16 ON p.player_id = e16.player_id
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

/* @@@@@@@@@@@@@@@@@ Optimized @@@@@@@@@@@@@@@@@ */

-- Q1 opt
SELECT p.player_name, AVG(e16.xg_score) AS avg_xg_score
FROM player p
JOIN event_16 e16 ON p.player_id = e16.player_id
WHERE e16.match_id IN (3764440, 3764661, 3773369, 3773372, 3773377, 3773386, 3773387, 3773403, 3773415, 3773428, 3773457, 3773466, 3773474, 3773477, 3773497, 3773523, 3773526, 3773547, 3773552, 3773565, 3773571, 3773585, 3773586, 3773587, 3773593, 3773597, 3773625, 3773631, 3773656, 3773660, 3773661, 3773665, 3773672, 3773689, 3773695)
GROUP BY p.player_name
ORDER BY avg_xg_score DESC;


-- Q2 opt
SELECT p.player_name, COUNT(e16.event_id) AS shots_count
FROM player p
JOIN event_16 e16 ON p.player_id = e16.player_id
WHERE e16.match_id IN (3764440, 3764661, 3773369, 3773372, 3773377, 3773386, 3773387, 3773403, 3773415, 3773428, 3773457, 3773466, 3773474, 3773477, 3773497, 3773523, 3773526, 3773547, 3773552, 3773565, 3773571, 3773585, 3773586, 3773587, 3773593, 3773597, 3773625, 3773631, 3773656, 3773660, 3773661, 3773665, 3773672, 3773689, 3773695)
GROUP BY p.player_name
ORDER BY shots_count DESC;

-- Q3 opt
SELECT p.player_name, COUNT(e16.event_id) AS first_time_shots
FROM player p
JOIN event_16 e16 ON p.player_id = e16.player_id
WHERE e16.match_id IN (15946, 15956, 15973, 15978, 15986, 15998, 16010, 16023, 16029, 16056, 16073, 16079, 16086, 16095, 16109, 16120, 16131, 16136, 16149, 16157, 16173, 16182, 16190, 16196, 16205, 16215, 16231, 16240, 16248, 16265, 16275, 16289, 16306, 16317, 303377, 303400, 303421, 303430, 303451, 303470, 303473, 303479, 303487, 303493, 303504, 303516, 303517, 303524, 303532, 303548, 303596, 303600, 303610, 303615, 303634, 303652, 303664, 303666, 303674, 303680, 303682, 303696, 303700, 303707, 303715, 303725, 303731, 3764440, 3764661, 3773372, 3773377, 3773386, 3773387, 3773403, 3773415, 3773428, 3773457, 3773466, 3773474, 3773477, 3773497, 3773523, 3773526, 3773547, 3773552, 3773565, 3773571, 3773585, 3773586, 3773587, 3773593, 3773597, 3773625, 3773631, 3773656, 3773660, 3773661, 3773665, 3773672, 3773689, 3773695)
AND e16.first_time = TRUE
GROUP BY p.player_name
ORDER BY first_time_shots DESC;

-- Q4 opt
SELECT t.team_name, COUNT(e30.event_30_id) AS passes_count
FROM team t
JOIN event_30 e30 ON t.team_id = e30.team_id
WHERE e30.match_id IN (3764440, 3764661, 3773369, 3773372, 3773377, 3773386, 3773387, 3773403, 3773415, 3773428, 3773457, 3773466, 3773474, 3773477, 3773497, 3773523, 3773526, 3773547, 3773552, 3773565, 3773571, 3773585, 3773586, 3773587, 3773593, 3773597, 3773625, 3773631, 3773656, 3773660, 3773661, 3773665, 3773672, 3773689, 3773695)
GROUP BY t.team_name
ORDER BY passes_count DESC;

-- Q5 opt
SELECT p.player_name, COUNT(e30.recipient_id) AS recipient_count
FROM player p
JOIN event_30 e30 ON p.player_id = e30.recipient_id
WHERE e30.match_id IN (3749052, 3749068, 3749079, 3749108, 3749117, 3749133, 3749153, 3749192, 3749196, 3749233, 3749246, 3749253, 3749257, 3749274, 3749276, 3749278, 3749296, 3749310, 3749346, 3749358, 3749360, 3749403, 3749431, 3749434, 3749448, 3749453, 3749454, 3749462, 3749465, 3749493, 3749522, 3749526, 3749528, 3749552, 3749590, 3749603, 3749631, 3749642)
GROUP BY p.player_name
ORDER BY recipient_count DESC;

-- Q6 opt
SELECT t.team_name, COUNT(e16.event_id) AS shots_count
FROM team t
JOIN event_16 e16 ON t.team_id = e16.team_id
WHERE e16.match_id IN (3749052, 3749068, 3749079, 3749108, 3749117, 3749133, 3749153, 3749192, 3749196, 3749233, 3749246, 3749253, 3749257, 3749274, 3749276, 3749278, 3749296, 3749310, 3749346, 3749358, 3749360, 3749403, 3749431, 3749434, 3749448, 3749453, 3749454, 3749462, 3749465, 3749493, 3749522, 3749526, 3749528, 3749552, 3749590, 3749603, 3749631, 3749642)
GROUP BY t.team_name
ORDER BY shots_count DESC;

-- Q7 opt
SELECT p.player_name, COUNT(e30.event_id) AS through_balls_count
FROM event_30 e30
JOIN player p ON e30.player_id = p.player_id 
WHERE e30.match_id IN (3764440, 3764661, 3773369, 3773372, 3773377, 3773386, 3773387, 3773403, 3773428, 3773457, 3773466, 3773474, 3773477, 3773497, 3773523, 3773526, 3773547, 3773552, 3773565, 3773571, 3773585, 3773586, 3773587, 3773593, 3773597, 3773625, 3773631, 3773656, 3773660, 3773661, 3773665, 3773672, 3773689, 3773695) 
AND e30.through_ball = True
GROUP BY p.player_name
ORDER BY through_balls_count DESC;

-- Q8 opt
SELECT t.team_name, COUNT(e30.event_id) AS through_balls_count
FROM event_30 e30
JOIN team t ON e30.team_id = t.team_id
WHERE e30.match_id IN (3764440, 3764661, 3773369, 3773372, 3773377, 3773386, 3773387, 3773403, 3773428, 3773457, 3773466, 3773474, 3773477, 3773497, 3773523, 3773526, 3773547, 3773552, 3773565, 3773571, 3773585, 3773586, 3773587, 3773593, 3773597, 3773625, 3773631, 3773656, 3773660, 3773661, 3773665, 3773672, 3773689, 3773695)
AND e30.through_ball = True
GROUP BY t.team_name
ORDER BY through_balls_count DESC;

-- Q9 opt
SELECT p.player_name, COUNT(e14.event_id) AS completed_dribbles
FROM player p
JOIN event_14 e14 ON p.player_id = e14.player_id
WHERE e14.match_id IN (15946, 15956, 15973, 15978, 15986, 15998, 16010, 16023, 16029, 16056, 16073, 16079, 16086, 16095, 16109, 16120, 16131, 16136, 16149, 16157, 16173, 16182, 16190, 16196, 16205, 16215, 16231, 16240, 16248, 16265, 16275, 16289, 16306, 16317, 303377, 303400, 303421, 303430, 303451, 303470, 303473, 303479, 303487, 303493, 303504, 303516, 303517, 303524, 303532, 303548, 303596, 303600, 303610, 303615, 303634, 303652, 303664, 303666, 303674, 303680, 303682, 303696, 303700, 303707, 303715, 303725, 303731, 3764440, 3764661, 3773369, 3773372, 3773377, 3773386, 3773387, 3773403, 3773415, 3773428, 3773457, 3773466, 3773474, 3773477, 3773497, 3773523, 3773526, 3773547, 3773552, 3773565, 3773571, 3773585, 3773586, 3773587, 3773593, 3773597, 3773625, 3773631, 3773656, 3773660, 3773661, 3773665, 3773672, 3773689, 3773695)
AND e14.complete = TRUE
GROUP BY p.player_name
ORDER BY completed_dribbles DESC;

-- Q10 opt
SELECT p.player_name, COUNT(e39.event_id) AS dribbled_past
FROM player p
JOIN event_39 e39 ON p.player_id = e39.player_id
WHERE e39.match_id IN (3764440, 3764661, 3773369, 3773372, 3773377, 3773386, 3773387, 3773403, 3773415, 3773428, 3773457, 3773466, 3773474, 3773477, 3773497, 3773523, 3773526, 3773547, 3773552, 3773565, 3773571, 3773585, 3773586, 3773587, 3773593, 3773597, 3773625, 3773631, 3773656, 3773660, 3773661, 3773665, 3773672, 3773689, 3773695)
GROUP BY p.player_name
ORDER BY dribbled_past ASC;

/* @@@@@@@@@@@@@@@@@ Denormalzied @@@@@@@@@@@@@@@@@ */

-- Q_1
SELECT p.player_name, AVG(e16.xg_score) AS avg_xg_score
FROM player p
JOIN event_16 e16 ON p.player_id = e16.player_id
WHERE e16.season_id = 90
GROUP BY p.player_name
ORDER BY avg_xg_score DESC;

-- Q_2
SELECT p.player_name, COUNT(e16.event_id) AS shots_count
FROM player p
JOIN event_16 e16 ON p.player_id = e16.player_id
WHERE e16.season_id = 90
GROUP BY p.player_name
ORDER BY shots_count DESC;

-- Q_3
SELECT p.player_name, COUNT(e16.event_id) AS first_time_shots
FROM player p
JOIN event_16 e16 ON p.player_id = e16.player_id
WHERE NOT e16.season_id = 42
AND e16.first_time = TRUE
GROUP BY p.player_name
ORDER BY first_time_shots DESC;

-- Q_4
SELECT t.team_name, COUNT(e30.event_id) AS passes_count
FROM team t
JOIN event_30 e30 ON t.team_id = e30.team_id
WHERE e30.season_id = 90
GROUP BY t.team_name
ORDER BY passes_count DESC;

-- Q_5
SELECT p.player_name, COUNT(e30.recipient_id) AS recipient_count
FROM player p
JOIN event_30 e30 ON p.player_id = e30.recipient_id
WHERE e30.season_id = 44
GROUP BY p.player_name
ORDER BY recipient_count DESC;

-- Q_6
SELECT t.team_name, COUNT(e16.event_id) AS shots_count
FROM team t
JOIN event_16 e16 ON t.team_id = e16.team_id
WHERE e16.season_id = 44
GROUP BY t.team_name
ORDER BY shots_count DESC;

-- Q_7
SELECT p.player_name, COUNT(e30.event_id) AS through_balls_count
FROM event_30 e30
JOIN player p ON e30.player_id = p.player_id 
WHERE e30.season_id = 90
AND e30.through_ball = True
GROUP BY p.player_name
ORDER BY through_balls_count DESC;

-- Q_8
SELECT t.team_name, COUNT(e30.event_id) AS through_balls_count
FROM event_30 e30
JOIN team t ON e30.team_id = t.team_id
WHERE e30.season_id = 90
AND e30.through_ball = True
GROUP BY t.team_name
ORDER BY through_balls_count DESC;

-- Q_9
SELECT p.player_name, COUNT(e14.event_id) AS completed_dribbles
FROM player p
JOIN event_14 e14 ON p.player_id = e14.player_id
WHERE e14.season_id IN (4, 42, 90)
AND e14.complete = TRUE
GROUP BY p.player_name
ORDER BY completed_dribbles DESC;

-- Q_10
SELECT p.player_name, COUNT(e39.event_id) AS dribbled_past
FROM player p
JOIN event_39 e39 ON p.player_id = e39.player_id
WHERE e39.season_id = 90
GROUP BY p.player_name
ORDER BY dribbled_past ASC;
