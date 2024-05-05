ALTER TABLE `univercity`.`relation`
ADD COLUMN `ToFamilyID` INT NOT NULL AFTER `ToPersonID`,
ADD CONSTRAINT `fk_relation_to_family` FOREIGN KEY (`ToFamilyID`) REFERENCES `univercity`.`family` (`FamilyID`);
