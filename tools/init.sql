-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema DiamondRough
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema DiamondRough
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `DiamondRough` DEFAULT CHARACTER SET utf8 ;
-- -----------------------------------------------------

-- -----------------------------------------------------
USE `DiamondRough` ;

-- -----------------------------------------------------
-- Table `DiamondRough`.`DIR_Tasks`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DiamondRough`.`DIR_Tasks` (
  `task_id` INT NOT NULL AUTO_INCREMENT,
  `task_name` VARCHAR(80) NOT NULL,
  `task_leader` VARCHAR(45) NOT NULL,
  `task_description` VARCHAR(250) NOT NULL,
  `creation_date` DATETIME NOT NULL,
  `modified_date` DATETIME NOT NULL,
  PRIMARY KEY (`task_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `DiamondRough`.`DIR_Personnel`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DiamondRough`.`DIR_Personnel` (
  `person_id` INT NOT NULL AUTO_INCREMENT,
  `user_name` VARCHAR(45) NOT NULL,
  `openID` VARCHAR(45) NULL,
  `last_name` INT NOT NULL,
  `first_name` VARCHAR(45) NOT NULL,
  `middle_name` VARCHAR(45) NULL,
  `gender` VARCHAR(10) NULL,
  `city` VARCHAR(45) NULL,
  `province_state` VARCHAR(45) NULL,
  `country` VARCHAR(45) NULL,
  `email_address` VARCHAR(100) NULL,
  `goal` VARCHAR(200) NULL,
  `executive_team_memeber` VARCHAR(10) NULL,
  `creation_date` DATETIME NULL,
  `modified_date` DATETIME NULL,
  PRIMARY KEY (`person_id`),
  UNIQUE INDEX `user_name_UNIQUE` (`user_name` ASC),
  UNIQUE INDEX `openID_UNIQUE` (`openID` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `DiamondRough`.`DIR_Task_Assignments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DiamondRough`.`DIR_Task_Assignments` (
  `person_id` INT NOT NULL,
  `task_id` INT NOT NULL,
  `creation_date` DATETIME NOT NULL,
  `modified_date` DATETIME NOT NULL,
  INDEX `fk_DIR_Task_Assignments_DIR_Tasks1_idx` (`task_id` ASC),
  PRIMARY KEY (`task_id`, `person_id`),
  INDEX `fk_DIR_Task_Assignments_DIR_Personnel1_idx` (`person_id` ASC),
  CONSTRAINT `fk_DIR_Task_Assignments_DIR_Tasks1`
    FOREIGN KEY (`task_id`)
    REFERENCES `DiamondRough`.`DIR_Tasks` (`task_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_DIR_Task_Assignments_DIR_Personnel1`
    FOREIGN KEY (`person_id`)
    REFERENCES `DiamondRough`.`DIR_Personnel` (`person_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `DiamondRough`.`DIR_Employment_History`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DiamondRough`.`DIR_Employment_History` (
  `person_id` INT NOT NULL,
  `employer_name` VARCHAR(100) NOT NULL,
  `employment_start_date` DATETIME NOT NULL,
  `job_title` VARCHAR(80) NOT NULL,
  `employment_end_date` DATETIME NULL,
  `creation_date` DATETIME NOT NULL,
  `modified_date` DATETIME NOT NULL,
  PRIMARY KEY (`employer_name`, `employment_start_date`, `person_id`),
  INDEX `fk_DIR_Employment_History_DIR_Personnel1_idx` (`person_id` ASC),
  CONSTRAINT `fk_DIR_Employment_History_DIR_Personnel1`
    FOREIGN KEY (`person_id`)
    REFERENCES `DiamondRough`.`DIR_Personnel` (`person_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `DiamondRough`.`DIR_Education_History`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DiamondRough`.`DIR_Education_History` (
  `person_id` INT NOT NULL,
  `college_name` VARCHAR(100) NOT NULL,
  `start_date` DATETIME NOT NULL,
  `major` VARCHAR(45) NOT NULL,
  `end_date` DATETIME NULL,
  `creation_date` DATETIME NOT NULL,
  `modified_date` DATETIME NOT NULL,
  PRIMARY KEY (`college_name`, `start_date`, `person_id`),
  INDEX `fk_DIR_Education_History_DIR_Personnel1_idx` (`person_id` ASC),
  CONSTRAINT `fk_DIR_Education_History_DIR_Personnel1`
    FOREIGN KEY (`person_id`)
    REFERENCES `DiamondRough`.`DIR_Personnel` (`person_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `DiamondRough`.`DIR_Teams`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DiamondRough`.`DIR_Teams` (
  `team_id` INT NOT NULL AUTO_INCREMENT,
  `team_name` VARCHAR(80) NOT NULL,
  `team_description` VARCHAR(100) NOT NULL,
  `creation_date` DATETIME NOT NULL,
  `modifed_date` DATETIME NOT NULL,
  PRIMARY KEY (`team_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `DiamondRough`.`DIR_Positions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DiamondRough`.`DIR_Positions` (
  `position_id` INT NOT NULL AUTO_INCREMENT,
  `position_name` VARCHAR(45) NOT NULL,
  `position_description` VARCHAR(100) NOT NULL,
  `creation_date` DATETIME NOT NULL,
  `modified_date` DATETIME NOT NULL,
  PRIMARY KEY (`position_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `DiamondRough`.`DIR_Team_Positions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DiamondRough`.`DIR_Team_Positions` (
  `team_id` INT NOT NULL,
  `position_id` INT NOT NULL,
  `creation_date` DATETIME NOT NULL,
  `modified_date` DATETIME NOT NULL,
  PRIMARY KEY (`position_id`, `team_id`),
  INDEX `fk_DIR_Team_Positions_DIR_Positions1_idx` (`position_id` ASC),
  INDEX `fk_DIR_Team_Positions_DIR_Teams1_idx` (`team_id` ASC),
  CONSTRAINT `fk_DIR_Team_Positions_DIR_Positions1`
    FOREIGN KEY (`position_id`)
    REFERENCES `DiamondRough`.`DIR_Positions` (`position_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_DIR_Team_Positions_DIR_Teams1`
    FOREIGN KEY (`team_id`)
    REFERENCES `DiamondRough`.`DIR_Teams` (`team_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `DiamondRough`.`DIR_Person_Position_Assignments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DiamondRough`.`DIR_Person_Position_Assignments` (
  `person_id` INT NOT NULL,
  `team_id` INT NULL,
  `position_id` INT NOT NULL,
  `creation_date` DATETIME NOT NULL,
  `modified_date` DATETIME NOT NULL,
  INDEX `fk_DIR_Person_Position_Assignments_DIR_Positions1_idx` (`position_id` ASC),
  INDEX `fk_DIR_Person_Position_Assignments_DIR_Personnel1_idx` (`person_id` ASC),
  INDEX `fk_DIR_Person_Position_Assignments_DIR_Teams1_idx` (`team_id` ASC),
  PRIMARY KEY (`person_id`, `team_id`, `position_id`),
  CONSTRAINT `fk_DIR_Person_Position_Assignments_DIR_Positions1`
    FOREIGN KEY (`position_id`)
    REFERENCES `DiamondRough`.`DIR_Positions` (`position_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_DIR_Person_Position_Assignments_DIR_Personnel1`
    FOREIGN KEY (`person_id`)
    REFERENCES `DiamondRough`.`DIR_Personnel` (`person_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_DIR_Person_Position_Assignments_DIR_Teams1`
    FOREIGN KEY (`team_id`)
    REFERENCES `DiamondRough`.`DIR_Teams` (`team_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;




SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
