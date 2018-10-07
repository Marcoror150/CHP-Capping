/*
Create statments for all initial users.
Marc Christensen
10/7/2018
Tested on MS SQL 2017
*/

INSERT INTO Users (Username, Password, First_Name, Last_Name, UserType)
VALUES ('root', 'root', 'root', 'root', 'root');

INSERT INTO Users (Username, Password, First_Name, Last_Name, UserType)
VALUES ('don_marie', 'password', 'Donnamarie', 'LastName', 'highUser');

INSERT INTO Users (Username, Password, First_Name, Last_Name, UserType)
VALUES ('drC', 'password', 'dr', 'c', 'viewOnly');