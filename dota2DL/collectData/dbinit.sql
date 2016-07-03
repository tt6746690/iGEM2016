-- MySQL Script generated by MySQL Workbench
-- Sat Jul  2 20:12:01 2016
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema dota2_data
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `dota2_data` ;

-- -----------------------------------------------------
-- Schema dota2_data
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `dota2_data` DEFAULT CHARACTER SET utf8 ;
USE `dota2_data` ;

-- -----------------------------------------------------
-- Table `dota2_data`.`Hero`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dota2_data`.`Hero` ;

CREATE TABLE IF NOT EXISTS `dota2_data`.`Hero` (
  `HERO_ID` INT NOT NULL,
  `LOCALIZED_NAME` VARCHAR(45) NULL,
  `NAME` VARCHAR(45) NULL,
  PRIMARY KEY (`HERO_ID`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
