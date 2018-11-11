CREATE TABLE Graph (
	GID			  int identity (1,1),
	Name		  VARCHAR (100) NOT NULL,
	Date_Created  DATE,
	Query		  VARCHAR (250) NOT NULL,
	PRIMARY KEY	  (GID)
);
