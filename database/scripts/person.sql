ALTER TABLE `univercity`.`person`
ADD COLUMN `Faculty` VARCHAR(50) NULL DEFAULT NULL AFTER `AVG`,
ADD COLUMN `Rating` INT NULL DEFAULT NULL AFTER `Faculty`,
ADD COLUMN `AlternativeLastName` VARCHAR(500) NULL AFTER `FamilyName`,
CHANGE COLUMN `Nickname` `Nickname` VARCHAR(100) NULL DEFAULT NULL ;