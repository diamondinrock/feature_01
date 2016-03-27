DELETE FROM diamondrough.dir_personnel;
ALTER TABLE diamondrough.dir_personnel AUTO_INCREMENT = 1;
LOAD DATA local INFILE "dir_personnel.txt"
INTO TABLE diamondrough.dir_personnel
FIELDS TERMINATED BY ','
       LINES TERMINATED BY '\n'
(user_name, openID, last_name, first_name, gender, city, province_state, country)
SET person_id = NULL;

DELETE FROM diamondrough.dir_team;
ALTER TABLE diamondrough.dir_team AUTO_INCREMENT = 1;
LOAD DATA LOCAL INFILE "dir_teams.txt"
INTO TABLE diamondrough.dir_team
FIELDS TERMINATED BY ','
       LINES TERMINATED BY '\n'
(team_name, team_description)
SET TEAM_ID = NULL;

DELETE FROM diamondrough.dir_task;
ALTER TABLE diamondrough.dir_task AUTO_INCREMENT = 1;
LOAD DATA LOCAL INFILE "dir_tasks.txt"
INTO TABLE diamondrough.dir_task
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(task_name, team_id, task_leader_id, task_description, signup_due_date)
SET TASK_ID = NULL;

DELETE FROM diamondrough.dir_task_assignment;
LOAD DATA LOCAL INFILE "dir_task_assignments.txt"
INTO TABLE diamondrough.dir_task_assignment
FIELDS TERMINATED BY ','
       LINES TERMINATED BY '\n'
(person_id, task_id, @creation_date, @modified_date)
SET creation_date = NOW(), modified_date = NOW();


