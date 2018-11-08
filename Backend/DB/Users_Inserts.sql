/*
Create statments for all initial users.
Marc Christensen
10/7/2018
Tested on MS SQL 2017
*/

INSERT INTO Users (Username, Password, First_Name, Last_Name, UserType)
VALUES ('root', 'root', 'root', 'root', 'Root');

INSERT INTO Users (Username, Password, First_Name, Last_Name, UserType)
VALUES ('don_marie', 'password', 'Donnamarie', 'LastName', 'Full User');

INSERT INTO Users (Username, Password, First_Name, Last_Name, UserType)
VALUES ('drC', 'password', 'dr', 'c', 'View Only');

INSERT INTO Users (Username, Password, First_Name, Last_Name, UserType)
VALUES ('Phillip', 'admin', 'Phillip', 'admin', 'Admin');

INSERT INTO Users (Username, Password, First_Name, Last_Name, UserType)
VALUES ('s_intern', 'password', 'super', 'intern', 'Super Intern');

INSERT INTO Users (Username, Password, First_Name, Last_Name, UserType)
VALUES ('intern1', 'password', 'intern', 'intern', 'Intern');