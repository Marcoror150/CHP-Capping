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
	KID		     int,
  ACEs_Score int,
  PRIMARY KEY (KID)
);

--Program Table
CREATE TABLE Program (
	PID		VARCHAR (3) NOT NULL,
  PRIMARY KEY (PID)
);

--ChildrenProgram Table
CREATE TABLE ChildrenProgram (
	KID 				int REFERENCES Children (KID),
  PID					VARCHAR (50) NOT NULL REFERENCES Program (PID),
  StartDate		DATE,
  EndDate			DATE,
  PRIMARY KEY (KID, PID, StartDate)
);

--IncidentTypes Table
CREATE TABLE IncidentTypes (
  TID   int identity (1,1),
  Name  VARCHAR (50) NOT NULL,
  PRIMARY KEY (TID)
);

--Incidents Table
CREATE TABLE Incidents (
  IID          int identity (1,1),
  KID          int REFERENCES Children (KID),
  M_In_Pgm     int,
  PRIMARY KEY (IID),
);

--IncidentClassification
CREATE TABLE IncidentClassification (
  IID  int REFERENCES Incidents (IID),
  TID  int REFERENCES IncidentTypes (TID),
  PRIMARY KEY (IID, TID)
);