/*
CHP Graph Database Definition
Used to store and recall saved data visualizations
Marc Christensen
12/3/2018
Tested on MS SQL 2017
*/

/* Delete table
DROP TABLE IF EXISTS Graph;
*/

CREATE TABLE Graph (
	GID			  INT identity (1,1),
	Name		  VARCHAR (100) NOT NULL,
	Date_Created  DATE DEFAULT getdate(),
	Query		  VARCHAR (250) NOT NULL,
	PRIMARY KEY	  (GID)
);
