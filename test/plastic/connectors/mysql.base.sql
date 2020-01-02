DROP DATABASE IF EXISTS `plastic_test`;

CREATE DATABASE `plastic_test`;

CREATE TABLE `plastic_test`.`task` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `active` BIT NULL DEFAULT 0,
  `title` VARCHAR(45) NOT NULL,
  `description` VARCHAR(45) NULL,
  PRIMARY KEY (`id`));

INSERT INTO `plastic_test`.`task` (`active`, `title`, `description`) VALUES (1, 'Some Task', 'A first thing to do.');
INSERT INTO `plastic_test`.`task` (`active`, `title`) VALUES (1, 'Another Thing');
INSERT INTO `plastic_test`.`task` (`title`) VALUES ('Skipped');
INSERT INTO `plastic_test`.`task` (`title`) VALUES ('Inactive');
INSERT INTO `plastic_test`.`task` (`title`, `description`) VALUES ('Uninteresting', 'Not much to say here.');
INSERT INTO `plastic_test`.`task` (`active`, `title`) VALUES (1, 'Very important');
