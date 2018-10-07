/*
CHP User Database Definition
Marc Christensen and Nick DePaul
10/7/2018
Tested on MS SQL 2017
*/

/* Drop every table
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS UserTypes;
*/


--UserTypes Table

CREATE TABLE UserTypes (
	UserType		  VARCHAR (50) NOT NULL,
  Description		VARCHAR (100) NOT NULL,
  PRIMARY KEY   (UserType)
);

--Users Table

CREATE TABLE Users (
  UID          int identity (1,1),
  Username     VARCHAR (50) NOT NULL,
  Password     VARCHAR (50) NOT NULL,
  First_Name   VARCHAR (50) NOT NULL,
  Last_Name    VARCHAR (50) NOT NULL,
  UserType     VARCHAR (50) NOT NULL REFERENCES UserTypes (UserType)
  PRIMARY KEY  (UID)
);
