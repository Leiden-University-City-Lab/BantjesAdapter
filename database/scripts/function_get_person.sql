SELECT *
FROM univercity.person p
JOIN univercity.location l ON l.locationPersonID = p.personPersonID AND p.TypeOfPerson = 1
WHERE ((FirstName LIKE '%Johannes%') AND (LastName LIKE '%ALBERTI%') AND ((SUBSTRING(l.locationStartDate, 1, 4) = '1698') OR (l.locationStartDate is null)) AND ((l.City = 'Assen') OR (l.City is null))) OR
		((LastName LIKE '%ALBERTI%') AND (SUBSTRING(l.locationStartDate, 1, 4) = '1698') AND ((l.City = 'Assen') OR (l.City is null))) OR
        ((LastName LIKE '%ALBERTI%') AND ((SUBSTRING(l.locationStartDate, 1, 4) = '1698') OR (l.locationStartDate is null)) AND (l.City = 'Assen'));
