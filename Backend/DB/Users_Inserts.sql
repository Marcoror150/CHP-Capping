/*
Create statments for all initial users.
Marc Christensen
10/7/2018
Tested on MS SQL 2017
*/

INSERT INTO Users (Username, Password, First_Name, Last_Name, UserType)
VALUES ('root', 'Password1!', 'root', 'root', 'Root');

INSERT INTO Users (Username, Password, First_Name, Last_Name, UserType)
VALUES ('donnamarie', 'Password1!', 'Donnamarie', 'Scorzello', 'Full User');

INSERT INTO Users (Username, Password, First_Name, Last_Name, UserType)
VALUES ('drC', 'Password1!', 'Doctor', 'Crenshaw', 'View Only');

INSERT INTO Users (Username, Password, First_Name, Last_Name, UserType)
VALUES ('Philip', 'Password1!', 'Philip', 'Edwards', 'Admin');

INSERT INTO Users (Username, Password, First_Name, Last_Name, UserType)
VALUES ('s_intern', 'Password1!', 'super', 'intern', 'Super Intern');

INSERT INTO Users (Username, Password, First_Name, Last_Name, UserType)
VALUES ('intern1', 'Password1!', 'intern', 'intern', 'Intern');