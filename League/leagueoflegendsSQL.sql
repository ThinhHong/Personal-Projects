CREATE DATABASE leagueoflegends;
DROP DATABASE leagueoflegends;
USE leagueoflegends;

CREATE TABLE IF NOT EXISTS player(
    id VARCHAR(80),
    account_id VARCHAR(80),
    puuid VARCHAR(80),
    name VARCHAR(25),
    profile_icon_id INTEGER,
    revision_date VARCHAR(30),
    summoner_level INTEGER,
    PRIMARY KEY (id,account_id,puuid,name)
);

CREATE TABLE IF NOT EXISTS champion(
    champion_id INTEGER,
    champion_name VARCHAR(15) NOT NULL,
    version VARCHAR(10) NOT NULL,
    attack INTEGER,
    defense INTEGER,
    magic INTEGER,
    difficulty INTEGER,
    PRIMARY KEY (champion_id,champion_name)
);

CREATE TABLE IF NOT EXISTS type(
    tags VARCHAR(10),
    champion_id INTEGER,
    PRIMARY KEY (champion_id,tags)
);

ALTER TABLE type
ADD FOREIGN KEY (champion_id)
REFERENCES champion(champion_id) ON DELETE CASCADE;

CREATE TABLE IF NOT EXISTS items(
    item_id INT,
    item_name VARCHAR(35),
    PRIMARY KEY (item_id) 
);



CREATE TABLE IF NOT EXISTS mastery(
    champion_id INT, 
    champion_level INT,
    champion_points INT,
    last_play_time VARCHAR(30),
    points_since_last_level INT,
    points_till_next_level INT,
    chest_granted TINYINT,
    tokens_earned INT,
    id VARCHAR(50),
    PRIMARY KEY(champion_id,id),
    FOREIGN KEY(champion_id) REFERENCES champion(champion_id) ON DELETE CASCADE,
    FOREIGN KEY(id) REFERENCES player(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS ranked(
    league_id VARCHAR(50),
    queue_type VARCHAR(15),
    tier VARCHAR(15),
    division VARCHAR(10),
    id VARCHAR(80),
    account_id VARCHAR(80),
    puuid VARCHAR(80),
    name VARCHAR(25),
    points INT,
    wins INT,
    loses INT,
    veteran TINYINT,
    inactive TINYINT,
    freshBlood TINYINT,
    streak TINYINT,
    PRIMARY KEY(league_id,id,account_id,puuid,name)
);


ALTER TABLE ranked
ADD FOREIGN KEY(id,account_id,puuid,name)
REFERENCES player(id,account_id,puuid,name)
ON DELETE CASCADE;


CREATE TABLE IF NOT EXISTS game(
    match_id VARCHAR(20),
    data_version VARCHAR(3),
    duration INT,
    game_id VARCHAR(30),
    mode VARCHAR(15),
    game_version VARCHAR(15),
    map_id INT,
    region VARCHAR(15),
    PRIMARY KEY (match_id)
);

CREATE TABLE IF NOT EXISTS match_history(
    match_id VARCHAR(40),
    id VARCHAR(80),
    account_id VARCHAR(80),
    puuid VARCHAR(80),
    name VARCHAR(30), 
    PRIMARY KEY (match_id,id,account_id,puuid,name),
    FOREIGN KEY (match_id) REFERENCES game(match_id) ON DELETE CASCADE, 
    FOREIGN KEY (id,account_id,puuid,name) REFERENCES player(id,account_id,puuid,name) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS participant(
    match_id VARCHAR(40),
    assist INT,
    champion_level INT,
    champion_id INT,
    champion_name VARCHAR(20),
    dmg_to_turrets INT,
    deaths INT,
    first_blood TINYINT,
    first_tower TINYINT,
    gold_spend INT,
    item0 INT,
    item1 INT,
    item2 INT,
    item3 INT,
    item4 INT,
    item5 INT,
    item6 INT,
    kills INT,
    participant_id INT,
    sumoner_level INT,
    id VARCHAR(80),
    team_position VARCHAR(10),
    total_damage INT,
    total_damage_taken INT,
    minions_killed INT,
    turret_kills INT,
    win TINYINT,
    PRIMARY KEY (match_id,champion_id,id),
    FOREIGN KEY (match_id) REFERENCES game(match_id) ON DELETE CASCADE,
    FOREIGN KEY (champion_id) REFERENCES champion(champion_id)ON DELETE CASCADE,
    FOREIGN KEY(id) REFERENCES player(id) ON DELETE CASCADE
);

ALTER TABLE participant
ADD COLUMN item0_name VARCHAR(35) AFTER item6,
ADD COLUMN item1_name VARCHAR(35) AFTER item0_name,
ADD COLUMN item2_name VARCHAR(35) AFTER item1_name,
ADD COLUMN item3_name VARCHAR(35) AFTER item2_name,
ADD COLUMN item4_name VARCHAR(35) AFTER item3_name,
ADD COLUMN item5_name VARCHAR(35) AFTER item4_name,
ADD COLUMN item6_name VARCHAR(35) AFTER item5_name;

DELIMITER $$
CREATE PROCEDURE getPlayerWinrate(IN player_name VARCHAR(30), OUT playrate DECIMAL(4,2))
BEGIN
	DECLARE played, games INT DEFAULT 0;
    DECLARE player VARCHAR(80);
    
    SELECT player.id INTO player
    FROM player
    WHERE player.name = player_name;
    
	SELECT count(*)
    INTO played
    FROM participant As p
    WHERE p.id = player AND p.win = 1;
    
    SELECT count(*)
    INTO games
    FROM participant AS p
    WHERE p.id = player;
    
    SELECT (played/games);
END $$
DELIMITER ;

SELECT * from player;
DELIMITER $$
CREATE PROCEDURE getChampionWinrate(IN champion_name VARCHAR(30), OUT winrate DECIMAL(4,2))
BEGIN
	DECLARE wins, games INT DEFAULT 0;
	SELECT count(*)
    INTO wins
    FROM participant AS P
    WHERE P.champion_name = champion_name AND P.win = 1;
    
    SELECT count(*)
    INTO games
    FROM participant AS P
    WHERE P.champion_name = champion_name;
    
    SELECT (wins/games);
END $$
DELIMITER ;

DROP PROCEDURE getChampionWinrate;

DELIMITER $$
CREATE PROCEDURE getChampionPlayrate(IN champion_name VARCHAR(30), OUT playrate DECIMAL(4,2))
BEGIN
	DECLARE played, games INT DEFAULT 0;
	SELECT count(*)
    INTO played
    FROM participant AS P
    WHERE P.champion_name = champion_name;
    
    SELECT count(DISTINCT match_id )
    INTO games
    FROM participant;
    
    SELECT (played/games);
END $$
DELIMITER ;

CALL GetChampionPlayrate("Leesin",@playrate);

DELIMITER $$
CREATE PROCEDURE getChampionPlayerWinrate(IN champion_name VARCHAR(30), IN player_name VARCHAR(30), OUT winrate DECIMAL(4,2))
BEGIN
	DECLARE wins, games INT DEFAULT 0;
    DECLARE playerid VARCHAR(90) DEFAULT "";
    
    SELECT player.id
    INTO playerid
    FROM player 
    WHERE player.name = player_name;
    
	SELECT count(*)
    INTO wins
    FROM participant AS P
    WHERE P.champion_name = champion_name AND P.win = 1 AND P.id = playerid;
    
    SELECT count(*)
    INTO games
    FROM participant AS P
    WHERE P.champion_name = champion_name AND P.id = playerid;
    
    SELECT (wins/games);
END $$

DELIMITER ;

DELIMITER $$
CREATE PROCEDURE getChampionRankWinrate(IN champion_name VARCHAR(30), IN tier VARCHAR(15), IN division VARCHAR(3), OUT winrate DECIMAL(4,2))
BEGIN
	DECLARE wins, games INT DEFAULT 0;

	SELECT count(*)
    INTO wins
    FROM participant AS P
    INNER JOIN ranked
    ON P.id = ranked.id
    WHERE P.champion_name = champion_name AND ranked.tier = tier AND ranked.division = division AND P.win = 1;
    
    SELECT count(*)
    INTO games
    FROM participant AS P
    INNER JOIN ranked
    ON P.id = ranked.id
    WHERE P.champion_name = champion_name AND ranked.tier = tier AND ranked.division = division;
    
    SELECT (wins/games);
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE itemPurchaseRate(IN item_name VARCHAR(35), IN tier VARCHAR(15), IN division VARCHAR(3), OUT purchase_rate DECIMAL(4,2))
BEGIN
DECLARE wins,total INT DEFAULT 0;

SELECT COUNT(p.win) INTO wins
FROM participant AS p
INNER JOIN ranked
ON p.id = ranked.id
WHERE (p.item0_name = item_name OR p.item1_name = item_name OR p.item2_name = item_name OR p.item3_name = item_name OR p.item4_name = item_name OR p.item5_name = item_name OR p.item6_name = item_name) AND p.win = 1 AND ranked.tier = tier AND ranked.division = division;

SELECT COUNT(*) INTO total
FROM participant AS p
INNER JOIN ranked
ON p.id = ranked.id;

SELECT(wins/total);

END $$
DELIMITER ;


CREATE PROCEDURE itemRankPurchaseRate
                
DELIMITER $$
CREATE PROCEDURE item_win_rate(IN item_name VARCHAR(35), OUT purchase_rate DECIMAL(4,2))
BEGIN
DECLARE wins,total INT DEFAULT 0;

SELECT COUNT(p.win) INTO wins
FROM participant AS p
WHERE (p.item0_name = item_name OR p.item1_name = item_name OR p.item2_name = item_name OR p.item3_name = item_name OR p.item4_name = item_name OR p.item5_name = item_name OR p.item6_name = item_name) AND p.win = 1;

SELECT COUNT(p.win) INTO total
FROM participant AS p
WHERE (p.item0_name = item_name OR p.item1_name = item_name OR p.item2_name = item_name OR p.item3_name = item_name OR p.item4_name = item_name OR p.item5_name = item_name OR p.item6_name = item_name);

SELECT(wins/total);

END $$
DELIMITER ;



DELIMITER $$
CREATE PROCEDURE top_champions(OUT champion VARCHAR(30), OUT total_win INT, OUT total_game_ INT, OUT win_rate DECIMAL(4,2))
BEGIN

	WITH wins AS(
SELECT
	p.champion_name, COUNT(p.champion_name) total_win
    FROM participant AS p
    WHERE p.win = 1
    GROUP BY p.champion_name
    ),
total AS (
    SELECT l.champion_name, total_win, COUNT(l.champion_name) total_game
    FROM participant AS l
    INNER JOIN wins AS w
    ON w.champion_name = l.champion_name
    GROUP BY w.champion_name)
	SELECT champion_name, total.total_win, total_game, total_win/total_game AS win_rate FROM total
    ORDER BY win_rate DESC
    LIMIT 5;
END$$
DELIMITER ;
CREATE PROCEDURE Topchampionwinrate(OUT champion_name VARCHAR(30), OUT winrate DECIMAL(4,2))
BEGIN
	DECLARE finished INT DEFAULT 0;
	DECLARE champ VARCHAR(30) DEFAULT "";
    DECLARE win DECIMAL(4,2) DEFAULT 0;
    
    DECLARE participant_cursor 
		CURSOR FOR 
			SELECT champion_name, win FROM participant;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;
    
    OPEN paricipant_cursor;
    
    get_participant: LOOP
			FETCH participant_cursor INTO champ,win;
            IF finished = 1 THEN
				LEAVE get_participant;
			END IF;
            SET win = win + 1
	FETCH participant_cursor INTO champ,win;
    CLOSE participant_cursor;
