ALTER TABLE `univercity`.`person`
ADD COLUMN `BirthDate` VARCHAR(50) NULL DEFAULT NULL AFTER `AVG`,
ADD COLUMN `BirthCountry` VARCHAR(50) NULL DEFAULT NULL AFTER `BirthDate`,
ADD COLUMN `BirthCity` VARCHAR(50) NULL DEFAULT NULL AFTER `BirthCountry`,
ADD COLUMN `BaptizedDate` VARCHAR(50) NULL DEFAULT NULL AFTER `BirthCity`,
ADD COLUMN `DeathDate` VARCHAR(50) NULL DEFAULT NULL AFTER `BaptizedDate`,
ADD COLUMN `DeathCity` VARCHAR(50) NULL DEFAULT NULL AFTER `DeathDate`,
ADD COLUMN `DeathCountry` VARCHAR(50) NULL DEFAULT NULL AFTER `DeathCity`,
ADD COLUMN `Faculty` VARCHAR(50) NULL DEFAULT NULL AFTER `DeathCountry`;


INSERT INTO univercity.type_of_relation (RelationID, RelationType)
VALUES
(1, 'Vader'),
(2, 'Moeder'),
(3, 'Grootvader'),
(4, 'Grootmoeder'),
(5, 'Vrouw'),
(6, 'Man'),
(7, 'Schoonvader'),
(8, 'Schoonmoeder'),
(9, 'Kind'),
(10, 'Verre familie');


INSERT INTO univercity.type_of_person (PersonID, PersonType)
VALUES
(3, 'Curator'),
(4, 'Staff');
