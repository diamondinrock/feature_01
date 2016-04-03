DELETE FROM diamondrough.dir_personnel;
ALTER TABLE diamondrough.dir_personnel AUTO_INCREMENT = 1;
LOAD DATA LOCAL INFILE "dir_personnel_data.txt"
INTO TABLE diamondrough.dir_personnel
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(person_id, user_name, last_name, first_name, city, occupation, creation_date, modified_date);

DELETE FROM diamondrough.dir_team;
ALTER TABLE diamondrough.dir_team AUTO_INCREMENT = 1;
LOAD DATA LOCAL INFILE "dir_team_data.txt"
INTO TABLE diamondrough.dir_team
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(team_id, team_name, team_description, creation_date, modified_date);

DELETE FROM diamondrough.dir_education_history;
ALTER TABLE diamondrough.dir_education_history AUTO_INCREMENT = 1;
LOAD DATA LOCAL INFILE "dir_education_history_data.txt"
INTO TABLE diamondrough.dir_education_history
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(person_id, college_name, college_start_date, major, creation_date, modified_date);

DELETE FROM diamondrough.dir_employment_history;
ALTER TABLE diamondrough.dir_employment_history AUTO_INCREMENT = 1;
LOAD DATA LOCAL INFILE "dir_employment_history_data.txt"
INTO TABLE diamondrough.dir_employment_history
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(person_id, employer_name, employment_start_date, job_title, creation_date, modified_date);

DELETE FROM diamondrough.dir_team_member;
ALTER TABLE diamondrough.dir_team_member AUTO_INCREMENT = 1;
LOAD DATA LOCAL INFILE "dir_team_member_data.txt"
INTO TABLE diamondrough.dir_team_member
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(person_id, team_id);

DELETE FROM diamondrough.dir_task;
ALTER TABLE diamondrough.dir_task AUTO_INCREMENT = 1;
LOAD DATA LOCAL INFILE "dir_task_data.txt"
INTO TABLE diamondrough.dir_task
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(task_id, team_id, task_name, task_description, signup_due_date, creation_date, modified_date);

DELETE FROM diamondrough.dir_task_assignment;
ALTER TABLE diamondrough.dir_task_assignment AUTO_INCREMENT = 1;
LOAD DATA LOCAL INFILE "dir_task_assignment_data.txt"
INTO TABLE diamondrough.dir_task_assignment
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(person_id, task_id, creation_date, modified_date);

