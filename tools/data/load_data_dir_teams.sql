
-- Be sure to place the dir_teams.txt in the right directory based on your database settings.

LOAD DATA INFILE "dir_teams.txt"
INTO TABLE DiamondRough.dir_teams
FIELDS TERMINATED BY ','
       LINES TERMINATED BY '\n'
(team_name, team_description)
SET TEAM_ID = NULL;


