#!/usr/bin/env python3
import pyodbc

# Connect to the db and return the connection and cursor for query execution
def connectToDB():
    try:
        # Connect to the db and capture its object
        # conn = pyodbc.connect('DSN=pochildrenshome;Trusted_Connection=yes;')
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=10.11.12.200;PORT=1433;DATABASE=POCHILDRENSHOME;UID=ChildrensHome;PWD=Capping2018!;')

        conn.setencoding('utf-8') 

        # Create a cursor from the connection object
        cur = conn.cursor()
        return conn, cur
    except:
        raise ValueError('Unable to connect to the database')

# Create a new table given a table name and the necessary columnspy
def createTable(table,columns):
    conn, cur = connectToDB()

    test1 = "dummy_table"
    test2 = ["Month","Means"]
    test3 = [[0.12,0.22],[0.3,0.5]]

    sql = """
        CREATE TABLE %s ( 
            %s int          NOT NULL,
            %s decimal(3,2) NOT NULL
        );
    """
    # Stitch together the function arguements to the sql statement
    sql = sql % (table, columns[0], columns[1])

    # Execute the query, commit changes and close the connection
    try:
        cur.execute(sql)
        conn.commit()
    except:
        conn.close()
        print('Unable to create table ' + table+ ' check if exists')
    
# Insert new entries into an existing table
def insertTable(table,columns,values):
    conn, cur = connectToDB()
    sql = """
        INSERT INTO %s (%s,%s) values(?,?);
    """

    # Stitch together the function arguements to the sql statement
    sql = sql % (table, columns[0], columns[1])

    # Execute the query, commit changes and close the connection
    try:
        cur.executemany(sql, values)
        conn.commit()
        conn.close()
    except:
        conn.close()
        raise ValueError('Unable to insert into table ' + table)

# Get all entries of a given table
def selectAll(table):
    conn, cur = connectToDB()
    sql = """
        SELECT * FROM dbo.%s;
    """
    # Stitch together the table to the sql statement
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
        raise ValueError('Table ' + table + ' does not exist')

# Get all tables in the db
def showAllTables():
    conn, cur = connectToDB()
    sql = """
        SELECT SYSSCHEMA.NAME, SYSTABLE.NAME
        FROM SYS.tables SYSTABLE
        INNER JOIN SYS.SCHEMAS SYSSCHEMA
        ON SYSTABLE.SCHEMA_ID = SYSSCHEMA.SCHEMA_ID;
    """
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

def query(query):
    conn, cur = connectToDB()
    sql = """
        %s
    """
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






