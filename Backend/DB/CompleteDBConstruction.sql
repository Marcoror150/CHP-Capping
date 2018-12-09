/*
CHP Complete Database Definition
Builds the entire backend database for CHP Incident system.
Marc Christensen
12/3/2018
Tested on MS SQL 2017
*/

/* Delete all tables
DROP TABLE IF EXISTS IncidentClassification;
DROP TABLE IF EXISTS Incidents;
DROP TABLE IF EXISTS IncidentTypes;
DROP TABLE IF EXISTS ChildrenProgram;
DROP TABLE IF EXISTS Program;
DROP TABLE IF EXISTS Children;
DROP TABLE IF EXISTS Graph;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS UserTypes;
DROP TRIGGER IF EXISTS removeRejectedEntries;
*/

--Graph Table
CREATE TABLE Graph (
	GID			  INT identity (1,1),
	Name		  VARCHAR (100) NOT NULL,
	Date_Created  DATE DEFAULT getdate(),
	Query		  VARCHAR (250) NOT NULL,
	PRIMARY KEY	  (GID)
);

--Children Table
CREATE TABLE Children (
  KID		 INT,
  ACEs_Score INT,
  PRIMARY KEY (KID)
);

--Program Table
CREATE TABLE Program (
  PID        VARCHAR (3) NOT NULL,
  PRIMARY KEY (PID)
);

--ChildrenProgram Table
CREATE TABLE ChildrenProgram (
  KID 			INT REFERENCES Children (KID),
  PID			VARCHAR (3) NOT NULL REFERENCES Program (PID),
  StartDate		DATE,
  EndDate		DATE,
  PRIMARY KEY (KID, PID, StartDate)
);

--UserTypes Table
CREATE TABLE UserTypes (
  UserType		    VARCHAR (50) NOT NULL,
  Description		VARCHAR (100) NOT NULL,
  PRIMARY KEY       (UserType)
);

--Users Table
CREATE TABLE Users (
  UID          INT identity (1,1),
  Username     VARCHAR (50) NOT NULL,
  Password     VARCHAR (50) NOT NULL,
  First_Name   VARCHAR (50) NOT NULL,
  Last_Name    VARCHAR (50) NOT NULL,
  UserType     VARCHAR (50) NOT NULL REFERENCES UserTypes (UserType)
  PRIMARY KEY  (UID)
);

--IncidentTypes Table
CREATE TABLE IncidentTypes (
  TID   INT identity (1,1),
  Name  VARCHAR (50) NOT NULL,
  PRIMARY KEY (TID)
);

--Incidents Table
CREATE TABLE Incidents (
  IID          INT identity (1,1),
  KID          INT REFERENCES Children (KID),
  M_In_Pgm     INT,
  Status       VARCHAR (15) DEFAULT 'NR',
  UID          INT REFERENCES Users (UID) NOT NULL,
  Date_Created DATE DEFAULT getdate(),
  PRIMARY KEY (IID),
);

--IncidentClassification
CREATE TABLE IncidentClassification (
  IID  INT REFERENCES Incidents (IID),
  TID  INT REFERENCES IncidentTypes (TID),
  PRIMARY KEY (IID, TID)
);

--Inserts for each table, all are required besides the user inserts, but one Root/Admin account must exist.

--UserTypes
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

--IncidentTypes
INSERT INTO IncidentTypes (Name)
VALUES ('Physical Assault');

INSERT INTO IncidentTypes (Name)
VALUES ('Sexually Aggressive Behavior');

INSERT INTO IncidentTypes (Name)
VALUES ('AWOLs');

INSERT INTO IncidentTypes (Name)
VALUES ('Self-Harm');

INSERT INTO IncidentTypes (Name)
VALUES ('Property Damage');

INSERT INTO IncidentTypes (Name)
VALUES ('Stealing');

INSERT INTO IncidentTypes (Name)
VALUES ('Weapons');

INSERT INTO IncidentTypes (Name)
VALUES ('Suicide Attempts');

INSERT INTO IncidentTypes (Name)
VALUES ('ER visits');

--Program
INSERT INTO Program (PID)
VALUES ('RTC');

INSERT INTO Program (PID)
VALUES ('YMP');

INSERT INTO Program (PID)
VALUES ('SHP');

INSERT INTO Program (PID)
VALUES ('ABH');

--Suggested User examples
INSERT INTO Users (Username, Password, First_Name, Last_Name, UserType)
VALUES ('root', 'root', 'root', 'root', 'Root');

INSERT INTO Users (Username, Password, First_Name, Last_Name, UserType)
VALUES ('donnamarie', 'password', 'Donnamarie', 'Scorzello', 'Full User');

INSERT INTO Users (Username, Password, First_Name, Last_Name, UserType)
VALUES ('drC', 'password', 'Doctor', 'Crenshaw', 'View Only');

INSERT INTO Users (Username, Password, First_Name, Last_Name, UserType)
VALUES ('Philip', 'admin', 'Philip', 'Edwards', 'Admin');

INSERT INTO Users (Username, Password, First_Name, Last_Name, UserType)
VALUES ('s_intern', 'password', 'super', 'intern', 'Super Intern');

INSERT INTO Users (Username, Password, First_Name, Last_Name, UserType)
VALUES ('intern1', 'password', 'intern', 'intern', 'Intern');

--Execute the trigger create statement after building the database
-- Trigger to remove rejected database entries
CREATE OR ALTER TRIGGER removeRejectedEntries ON Incidents
AFTER UPDATE
AS
BEGIN
  -- Store IID to delete from both tables
  DECLARE @IIDToDelete INT
  SET @IIDToDelete = (SELECT IID FROM Incidents WHERE Status = 'R')
  
  -- Trigger Code
  DELETE FROM IncidentClassification WHERE IID = @IIDToDelete
  DELETE FROM Incidents WHERE IID = @IIDToDelete
END
GO 