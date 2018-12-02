CREATE TABLE Graph (
	GID			  INT identity (1,1),
	Name		  VARCHAR (100) NOT NULL,
	Date_Created  DATE DEFAULT getdate(),
	Query		  VARCHAR (250) NOT NULL,
	PRIMARY KEY	  (GID)
);
