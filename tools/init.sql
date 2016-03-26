-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema diamondrough
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema diamondrough
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `diamondrough` DEFAULT CHARACTER SET utf8 ;
USE `diamondrough` ;

-- -----------------------------------------------------
-- Table `diamondrough`.`dir_personnel`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `diamondrough`.`dir_personnel` (
  `person_id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_name` VARCHAR(45) NOT NULL,
  `openID` VARCHAR(45) NULL DEFAULT NULL,
  `header_url` VARCHAR(200) NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `first_name` VARCHAR(45) NOT NULL,
  `middle_name` VARCHAR(45) NULL DEFAULT NULL,
  `gender` VARCHAR(10) NULL DEFAULT NULL,
  `city` VARCHAR(45) NOT NULL,
  `province_state` VARCHAR(45) NULL DEFAULT NULL,
  `country` VARCHAR(45) NULL DEFAULT NULL,
  `occupation` VARCHAR(45) NOT NULL,
  `email_address` VARCHAR(100) NULL DEFAULT NULL,
  `self_introduction` VARCHAR(1000) NULL,
  `executive_team_member` VARCHAR(10) NULL DEFAULT NULL,
  `creation_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`person_id`),
  UNIQUE INDEX `user_name_UNIQUE` (`user_name` ASC),
  UNIQUE INDEX `openID_UNIQUE` (`openID` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `diamondrough`.`dir_education_history`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `diamondrough`.`dir_education_history` (
  `person_id` INT(11) NOT NULL,
  `college_name` VARCHAR(100) NOT NULL,
  `college_start_date` DATETIME NOT NULL,
  `major` VARCHAR(45) NOT NULL,
  `college_end_date` DATETIME NULL,
  `creation_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`college_name`, `college_start_date`, `person_id`),
  INDEX `fk_dir_education_history_dir_personnel1_idx` (`person_id` ASC),
  CONSTRAINT `fk_dir_education_history_dir_personnel1`
    FOREIGN KEY (`person_id`)
    REFERENCES `diamondrough`.`dir_personnel` (`person_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `diamondrough`.`dir_employment_history`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `diamondrough`.`dir_employment_history` (
  `person_id` INT(11) NOT NULL,
  `employer_name` VARCHAR(100) NOT NULL,
  `employment_start_date` DATETIME NOT NULL,
  `job_title` VARCHAR(80) NOT NULL,
  `employment_end_date` DATETIME NULL DEFAULT NULL,
  `creation_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`employer_name`, `employment_start_date`, `person_id`),
  INDEX `fk_dir_employment_history_dir_personnel1_idx` (`person_id` ASC),
  CONSTRAINT `fk_dir_employment_history_dir_personnel1`
    FOREIGN KEY (`person_id`)
    REFERENCES `diamondrough`.`dir_personnel` (`person_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `diamondrough`.`dir_team`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `diamondrough`.`dir_team` (
  `team_id` INT(11) NOT NULL AUTO_INCREMENT,
  `team_name` VARCHAR(80) NOT NULL,
  `team_leader_id` INT(11) NULL,
  `team_description` VARCHAR(100) NOT NULL,
  `creation_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`team_id`),
  INDEX `fk_dir_team_dir_personnel1_idx` (`team_leader_id` ASC),
  CONSTRAINT `fk_dir_team_dir_personnel1`
    FOREIGN KEY (`team_leader_id`)
    REFERENCES `diamondrough`.`dir_personnel` (`person_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `diamondrough`.`dir_task`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `diamondrough`.`dir_task` (
  `task_id` INT(11) NOT NULL AUTO_INCREMENT,
  `team_id` INT(11) NOT NULL,
  `task_name` VARCHAR(80) NOT NULL,
  `task_leader_id` INT(11) NULL,
  `task_description` VARCHAR(250) NOT NULL,
  `signup_due_date` DATE NOT NULL,
  `completion_date` DATE NULL,
  `creation_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`task_id`, `team_id`),
  INDEX `fk_dir_tasks_dir_teams1_idx` (`team_id` ASC),
  INDEX `fk_dir_task_dir_personnel1_idx` (`task_leader_id` ASC),
  CONSTRAINT `fk_dir_tasks_dir_teams1`
    FOREIGN KEY (`team_id`)
    REFERENCES `diamondrough`.`dir_team` (`team_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_dir_task_dir_personnel1`
    FOREIGN KEY (`task_leader_id`)
    REFERENCES `diamondrough`.`dir_personnel` (`person_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `diamondrough`.`dir_task_assignment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `diamondrough`.`dir_task_assignment` (
  `person_id` INT(11) NOT NULL,
  `task_id` INT(11) NOT NULL,
  `comments` VARCHAR(100) NULL,
  `creation_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`person_id`, `task_id`),
  INDEX `fk_dir_task_assignments_dir_tasks1_idx` (`task_id` ASC),
  INDEX `fk_dir_task_assignments_dir_personnel1_idx` (`person_id` ASC),
  CONSTRAINT `fk_dir_task_assignments_dir_personnel1`
    FOREIGN KEY (`person_id`)
    REFERENCES `diamondrough`.`dir_personnel` (`person_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_dir_task_assignments_dir_tasks1`
    FOREIGN KEY (`task_id`)
    REFERENCES `diamondrough`.`dir_task` (`task_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `diamondrough`.`dir_team_member`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `diamondrough`.`dir_team_member` (
  `person_id` INT(11) NOT NULL,
  `team_id` INT(11) NOT NULL,
  `member_status` VARCHAR(45) NULL,
  `contact_information` VARCHAR(80) NULL,
  `self_introduction` VARCHAR(1000) NULL,
  `creation_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`person_id`, `team_id`),
  INDEX `fk_dir_team_members_dir_teams1_idx` (`team_id` ASC),
  CONSTRAINT `fk_dir_team_members_dir_personnel1`
    FOREIGN KEY (`person_id`)
    REFERENCES `diamondrough`.`dir_personnel` (`person_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_dir_team_members_dir_teams1`
    FOREIGN KEY (`team_id`)
    REFERENCES `diamondrough`.`dir_team` (`team_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
