/*
CHP Incident Database Definition
Marc Christensen and Nick DePaul
10/7/2018
Tested on MS SQL 2017
*/

/* Delete all tables
DROP TABLE IF EXISTS Incidents;
DROP TABLE IF EXISTS IncidentTypes;
DROP TABLE IF EXISTS ChildrenProgram;
DROP TABLE IF EXISTS IncidentClassification;
DROP TABLE IF EXISTS Program;
DROP TABLE IF EXISTS Children;
*/

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
  PID			VARCHAR (50) NOT NULL REFERENCES Program (PID),
  StartDate		DATE,
  EndDate		DATE,
  PRIMARY KEY (KID, PID, StartDate)
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
  Status       VARCHAR (15) NOT NULL,
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

-- Trigger to remove rejected database entries
CREATE OR ALTER TRIGGER removeRejectedEntries ON Incidents
AFTER UPDATE
AS
BEGIN
  -- Store IID to delete from both tables
  DECLARE @IIDToDelete INT
  SET @IIDToDelete = (SELECT IID FROM Incidents WHERE Status = 'Rejected')
  
  -- Trigger Code
  DELETE FROM IncidentClassification WHERE IID = @IIDToDelete
  DELETE FROM Incidents WHERE IID = @IIDToDelete
END
GO
