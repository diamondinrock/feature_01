LOAD DATA INFILE "DIR_Tasks.txt"
INTO TABLE DiamondRough.DIR_Tasks
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(task_name, task_leader, task_description, creation_date, modified_date)
SET TASK_ID = NULL;
