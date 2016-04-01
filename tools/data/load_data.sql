DELETE FROM dir_personnel;
LOAD DATA LOCAL INFILE "dir_personnel_data.txt"
INTO TABLE diamondrough.dir_personnel
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(person_id, user_name, last_name, first_name, city, occupation, creation_date, modified_date);

DELETE FROM dir_team;
LOAD DATA LOCAL INFILE "dir_team_data.txt"
INTO TABLE diamondrough.dir_team
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(team_id, team_name, team_description, creation_date, modified_date);

DELETE FROM dir_education_history;
LOAD DATA LOCAL INFILE "dir_education_history_data.txt"
INTO TABLE diamondrough.dir_education_history
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(person_id, college_name, college_start_date, major, creation_date, modified_date);

DELETE FROM dir_employment_history;
LOAD DATA LOCAL INFILE "dir_employment_history_data.txt"
INTO TABLE diamondrough.dir_employment_history
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(person_id, employer_name, employment_start_date, job_title, creation_date, modified_date);

DELETE FROM dir_team_member;
LOAD DATA LOCAL INFILE "dir_team_member_data.txt"
INTO TABLE diamondrough.dir_team_member
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(person_id, team_id);

DELETE FROM dir_task;
LOAD DATA LOCAL INFILE "dir_task_data.txt"
INTO TABLE diamondrough.dir_task
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(task_id, team_id, task_name, task_description, signup_due_date, creation_date, modified_date);

DELETE FROM dir_task_assignment;
LOAD DATA LOCAL INFILE "dir_task_assignment_data.txt"
INTO TABLE diamondrough.dir_task_assignment
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(person_id, task_id, creation_date, modified_date);

