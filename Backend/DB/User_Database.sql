--UserTypes Table

CREATE TABLE UserTypes (
	Type					VARCHAR NOT NULL,
  Description		CHAR(25)
  PRIMARY KEY  (Type)
);

--Users Table

CREATE TABLE Users (
  UID          int identity (1,1),
  Username     VARCHAR NOT NULL,
  Password     VARCHAR NOT NULL,
  First_Name   VARCHAR NOT NULL,
  Last_Name    VARCHAR NOT NULL,
  Acc_Type     VARCHAR NOT NULL REFERENCES UserTypes (Type)
  PRIMARY KEY  (UID)
);
