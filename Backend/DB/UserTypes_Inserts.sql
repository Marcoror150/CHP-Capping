/*
Create statments for all user types.
Marc Christensen
10/7/2018
Tested on MS SQL 2017
*/

INSERT INTO UserTypes (UserType, Description)
VALUES ('Root', 'Root user, complete control.');

INSERT INTO UserTypes (UserType, Description)
VALUES ('Admin', 'Manage accounts and database.');

INSERT INTO UserTypes (UserType, Description)
VALUES ('Full User', 'Can insert/delete incidents to database and can create/remove reports.');

INSERT INTO UserTypes (UserType, Description)
VALUES ('Super Intern', 'Can insert incidents to database and can create reports.');

INSERT INTO UserTypes (UserType, Description)
VALUES ('Intern', 'Suggests poetential incidents and can create reports.');

INSERT INTO UserTypes (UserType, Description)
VALUES ('View Only', 'User can generate and view reports only.');