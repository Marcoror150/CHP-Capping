/*
Create statments for all user types.
Marc Christensen
10/7/2018
Tested on MS SQL 2017
*/

INSERT INTO UserTypes (UserType, Description)
VALUES ('root', 'Root user, complete control.');

INSERT INTO UserTypes (UserType, Description)
VALUES ('admin', 'Manage accounts and database.');

INSERT INTO UserTypes (UserType, Description)
VALUES ('highUser', 'Can insert/delete incidents to database and can create/remove reports.');

INSERT INTO UserTypes (UserType, Description)
VALUES ('superIntern', 'Can insert incidents to database and can create reports.');

INSERT INTO UserTypes (UserType, Description)
VALUES ('intern', 'Suggests poetential incidents and can create reports.');

INSERT INTO UserTypes (UserType, Description)
VALUES ('viewOnly', 'User can generate and view reports only.');