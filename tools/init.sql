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
  `openID` VARCHAR(45) NOT NULL,
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
  `DIR_Personnel_person_id` INT NOT NULL,
  `DIR_Tasks_task_id` INT NOT NULL,
  PRIMARY KEY (`person_id`, `task_id`),
  INDEX `fk_DIR_Task_Assignments_DIR_Personnel_idx` (`DIR_Personnel_person_id` ASC),
  INDEX `fk_DIR_Task_Assignments_DIR_Tasks1_idx` (`DIR_Tasks_task_id` ASC),
  CONSTRAINT `fk_DIR_Task_Assignments_DIR_Personnel`
    FOREIGN KEY (`DIR_Personnel_person_id`)
    REFERENCES `DiamondRough`.`DIR_Personnel` (`person_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_DIR_Task_Assignments_DIR_Tasks1`
    FOREIGN KEY (`DIR_Tasks_task_id`)
    REFERENCES `DiamondRough`.`DIR_Tasks` (`task_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
