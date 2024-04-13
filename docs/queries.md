1. In the La Liga season of 2020/2021, sort the players from highest to lowest based on their average xG scores. **Output both the player names and their average xG scores.**
    - `event_16`
2. In the La Liga season of 2020/2021, find the players with the most shots. Sort them from highest to lowest. **Output both the player names and the number of shots.**
    - `event_16`
3. In the La Liga seasons of 2020/2021, 2019/2020, and 2018/2019 combined, find the players with the most first-time shots. Sort them from highest to lowest. **Output the player names and the number of first time shots.**
    - `event_16`
4. In the La Liga season of 2020/2021, find the teams with the most passes made. Sort them from highest to lowest. **Output the team names and the number of passes.**
    - `event_30`
5. In the Premier League season of 2003/2004, find the players who were the most intended recipients of passes. Sort them from highest to lowest. **Output the player names and the number of times they were the intended recipients of passes.**
    - `event_30`
6. In the Premier League season of 2003/2004, find the teams with the most shots made. Sort them from highest to lowest. **Output the team names and the number of shots.**
    - `event_16`
7. In the La Liga season of 2020/2021, find the players who made the most through balls. Sort them from highest to lowest. **Output the player names and the number of through balls.**
    - `event_30` and `through_ball = true`
8. In the La Liga season of 2020/2021, find the teams that made the most through balls. Sort them from highest to lowest. **Output the team names and the number of through balls.**
    - `event_30` and `pass_technique_id = 108`
9. In the La Liga seasons of 2020/2021, 2019/2020, and 2018/2019 combined, find the players that were the most successful in completed dribbles. Sort them from highest to lowest. **Output the player names and the number of successful completed dribbles.**
    - `event_14` , look up `related_event` with `type = 14` and find ones where `complete = true`
10. In the La Liga season of 2020/2021, find the players that were least dribbled past. Sort them from lowest to highest. **Output the player names and the number of dribbles.**
    - `event_39`



```diff
-- Ball Recovery
-- Dispossessed
-- Duel
-- Camera On
-- Block
-- Offside
-- Clearance
-- Interception
++ Dribble
++ Shot
-- Pressure
-- Half Start
-- Substitution
-- Own Goal Against
-- Foul Won
-- Foul Committed
++ Goal Keeper
-- Bad Behaviour
-- Own Goal For
-- Player On
-- Player Off
-- Shield
-- Camera off
++ Pass
-- 50/50
-- Half End
-- Starting XI
-- Tactical Shift
-- Error
-- Miscontrol
++ Dribbled Past
-- Injury Stoppage
-- Referee Ball-Drop
-- Ball Receipt*
-- Carry
```

