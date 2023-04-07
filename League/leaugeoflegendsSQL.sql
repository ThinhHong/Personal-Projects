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

select * from champion;
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
    summoner_level INT,
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



DROP procedure IF EXISTS `champion_winrate`;
DELIMITER $$
USE `leagueoflegends`$$
CREATE PROCEDURE `champion_winrate` (IN champion_name VARCHAR(20))
BEGIN
SELECT COUNT(part.win) FROM participant as part WHERE part.win = 1 AND part.champion_name = champion_name;
END$$
DELIMITER ;
                        
