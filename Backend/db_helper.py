#!/usr/bin/env python3

# Helper functions that connects Python to the database
# Michael Gutierrez
# 10/16/2018

import pyodbc

# Connect to the db and return the connection and cursor for query execution
def connectToDB():
    try:
        # Connect to the db and capture its object
        conn = pyodbc.connect('DSN=pochildrenshome;UID=ChildrensHome;PWD=Capping2018!;')

        # conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=10.11.12.200,1433;DATABASE=POCHILDRENSHOME;UID=ChildrensHome;PWD=Capping2018!;')

        conn.setencoding('utf-8') 

        # Create a cursor from the connection object
        cur = conn.cursor()
        return conn, cur
    except:
        raise ValueError('Unable to connect to the database')

# Check if a given table exists in the db
def tableExists(table):
    conn, cur = connectToDB()

    # Tables come back from db as list of tuples
    tables = getAllTables()
    
    # Loop through to find the table
    for tup in tables:
        if table in tup:
            return True
    else:
        return False 

# Get all columns of a given table
def getTableCols(table):
    conn, cur = connectToDB()

    # Query to get all columns excpet those that are serializable 
    sql = """
        SELECT c.name 
        FROM sys.columns c
        JOIN sys.tables AS t
        ON t.object_id=c.object_id
        WHERE c.name NOT IN(
            SELECT name 
            FROM sys.identity_columns
            WHERE is_identity=1)
        AND  t.name='%s'
    """
    # Stitch together the sql query
    sql = sql % (table)

     # Execute the query and close the connection and return the results
    try:
        cur.execute(sql)
        entries = cur.fetchall()
        conn.close()
        return entries
    except:
        conn.close()

# Insert new entries into an existing table
def insertTable(table,values):
    conn, cur = connectToDB()

    # Check if the table exists first
    if not tableExists(table):
        raise ValueError('Table:%s does not exist' %table)

    # Unpack the columns because they come in as a list of tuples
    columns = [col for tupl in getTableCols(table) for col in tupl]

    sql = """
        INSERT INTO %s (%s) values(%s);
    """
    columns_sql = ','.join(columns)
    values_sql = ','.join(['?' for i in range(len(columns))])

    # Stitch together the sql query
    sql = sql % (table, columns_sql,values_sql)

    # Execute the query, commit changes and close the connection
    try:
        cur.executemany(sql, values)
        conn.commit()
        conn.close()
    except ValueError:
        conn.close()
        print('Unable to insert into table %s, check proper values or duplicate values' %table)

# Get all entries of a given table
def selectAll(table):
    conn, cur = connectToDB()
    sql = """
        SELECT * FROM %s;
    """

    # Stitch together the sql query
    sql = sql % (table)

    # Execute the query and close the connection
    try:
        cur.execute(sql)

        # Iterate through the cursor results if there are any
        entries = cur.fetchall()
        if not entries:
            print('No entries')
            return
        # Print all entries to check
        for entry in entries:
            print(entry)
        conn.close()

    except:
        conn.close()
        raise ValueError('Table:%d does not exist' %table)

# Get all tables in the db
def getAllTables():
    conn, cur = connectToDB()
    sql = """
        SELECT [name]
        FROM sys.tables
        WHERE create_date > Convert(datetime,'2018-01-01')
    """
    # Execute the query and close the connection
    try:
        cur.execute(sql)
        # Iterate through the cursor results if there are any
        entries = cur.fetchall()
        conn.close()
        return entries
    except:
        conn.close()
# Run any general query
def query(query):
    conn, cur = connectToDB()
    sql = """
        %s
    """
    # Stitch together the sql query
    sql = sql % (query)

    # Execute the query and close the connection
    try:
        cur.execute(sql)

        # Iterate through the cursor results if there are any
        entries = cur.fetchall()
        if not entries:
            print('No entries')
            return
        # Print all entries to check
        for entry in entries:
            print(entry)

        conn.close()
    except:
        conn.close()

def validateLogin(uname,pwd):
	conn, cur = connectToDB()
	sql = "SELECT * FROM Users WHERE username = '"+uname+"' AND password = '"+pwd+"';"
	print (sql)
	try:
		cur.execute(sql)
		
		entries = cur.fetchall()
		if not entries:
			return False
		else:
			for entry in entries:
				print (entry)
			return True
		
		conn.close()
	except:
		conn.close()

# Get the id given an incedent name
def getTID(name):
    conn, cur = connectToDB()
    sql = """
        SELECT TID
        FROM IncidentTypes
        WHERE name = '%s'
    """
    # Stitch together the sql query
    sql = sql % (name)

    # Execute the query and close the connection
    try:
        cur.execute(sql)

        # Check if IncidentType exists
        entry = cur.fetchall()
        if not entries:
            conn.close()
            print('No entries')
            return
        else:
            conn.close()
            return entry
    except:
        conn.close()
# Get latest id of the table last inserted to
def getLastID():
    conn, cur = connectToDB()
    sql = """
        SELECT SCOPE_IDENTITY()
    """
    # Execute the query and close the connection
    try:
        cur.execute(sql)

        # Check if IncidentType exists
        entry = cur.fetchall()
        if not entries:
            conn.close()
            print('No entries')
            return
        else:
            conn.close()
            return entry
    except:
        conn.close()

