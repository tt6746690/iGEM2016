-- MySQL Script generated by MySQL Workbench
-- Sun Jul  3 14:33:36 2016
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


-- -----------------------------------------------------
-- Table `dota2_data`.`GameMatch`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dota2_data`.`GameMatch` ;

CREATE TABLE IF NOT EXISTS `dota2_data`.`GameMatch` (
  `MATCH_ID` BIGINT(8) NOT NULL,
  `RADIANT_WIN` TINYINT(1) NULL,
  PRIMARY KEY (`MATCH_ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dota2_data`.`MatchPlayer`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dota2_data`.`MatchPlayer` ;

CREATE TABLE IF NOT EXISTS `dota2_data`.`MatchPlayer` (
  `MATCHPLAYER_ID` INT NOT NULL AUTO_INCREMENT,
  `ACCOUNT_ID` BIGINT(8) NULL,
  `HERO_ID` INT NULL,
  `HERO_NAME` VARCHAR(45) NULL,
  `TEAM_ID` INT NULL COMMENT '0-radiant, 1-dire, 2-broadcasters',
  `MATCH_ID` BIGINT(8) NOT NULL,
  PRIMARY KEY (`MATCHPLAYER_ID`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
