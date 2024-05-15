SELECT *
FROM univercity.person p
JOIN univercity.location l ON l.locationPersonID = p.personPersonID AND p.TypeOfPerson = 1
LEFT OUTER JOIN univercity.type_of_location tol ON tol.LocationID = l.TypeOfLocation
LEFT OUTER JOIN univercity.relation rel ON p.personPersonID = rel.FromPersonID
LEFT OUTER JOIN univercity.type_of_relation tor ON rel.RelationID = tor.RelationID -- Joining type_of_relation through relation
LEFT OUTER JOIN univercity.education edu ON p.personPersonID = edu.personPersonID
LEFT OUTER JOIN univercity.career car ON p.personPersonID = car.personPersonID
LEFT OUTER JOIN univercity.type_of_person top ON p.TypeOfPerson = top.PersonID
LEFT OUTER JOIN univercity.particularity par ON p.personPersonID = par.personPersonID

WHERE ((p.FirstName LIKE '%Johannes%') AND (p.LastName LIKE '%ALBERTI%') AND ((SUBSTRING(l.locationStartDate, 1, 4) = '1698') OR (l.locationStartDate is null)) AND ((l.City = 'Assen') OR (l.City is null))) OR
		((p.LastName LIKE '%ALBERTI%') AND (SUBSTRING(l.locationStartDate, 1, 4) = '1698') AND ((l.City = 'Assen') OR (l.City is null))) OR
        ((p.LastName LIKE '%ALBERTI%') AND ((SUBSTRING(l.locationStartDate, 1, 4) = '1698') OR (l.locationStartDate is null)) AND (l.City = 'Assen'));
