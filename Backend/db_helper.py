#!/usr/bin/env python3

# Helper functions that connects Python to the database
# Michael Gutierrez
# 10/16/2018

import pyodbc
from flask import flash

# Connect to the db and return the connection and cursor for query execution
def connectToDB():
    try:
        # Connect to the db and capture its object
        conn = pyodbc.connect('DSN=pochildrenshome;UID=ChildrensHome;PWD=!Capping2018;')

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
def getTableCols(table, showSerial):
    conn, cur = connectToDB()
    sql = ""
    if showSerial == False:

        # Query to get all columns except those that are serializable 
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
    else:
        # Query to get all columns
        sql = """
            SELECT [name] 
            FROM sys.columns 
            WHERE object_id = OBJECT_ID('%s') 
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
    columns = [col for tupl in getTableCols(table,False) for col in tupl]

    sql = """
        INSERT INTO %s values(%s);
    """
    # columns_sql = ','.join(columns)
    values_sql = ','.join(['?' for i in range(len(values))])

    # Stitch together the sql query
    sql = sql % (table,values_sql)

    # Execute the query, commit changes and close the connection
    try:
        cur.execute(sql, values)
        conn.commit()
        conn.close()
    except ValueError:
        conn.close()
        print('Unable to insert into table %s, check proper values or duplicate values' %table)

# Get all entries of a given table
def getTable(table):
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
        conn.close()
        if not entries:
            print('No entries')
            return
        return entries

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
        # Check if there are any results
        entries = cur.fetchall()
        conn.close()
        return entries
    except Exception as e: 
        print(e)
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
    except Exception as e: 
        print(e)
        conn.close()

# Run any general query
def countChildren():
    conn, cur = connectToDB()
    sql = """
        SELECT count(KID)
        FROM Children
    """
    # Execute the query and close the connection
    try:
        cur.execute(sql)

        # Iterate through the cursor results if there are any
        count = cur.fetchall()
        conn.close()
        if not count:
            print('No entries')
            return
        return count[0][0]
    
    except Exception as e: 
        print(e)
        conn.close()


# Get children associated with a given program
def getChildrenProgram(program):
    conn, cur = connectToDB()
    sql = """
        SELECT *
        FROM ChildrenProgram
        WHERE PID in (
            SELECT PID
            FROM Program
            WHERE PID ='%s'
        )
    """
    # Stitch together the sql query
    sql = sql % (program)

    # Execute the query and close the connection
    try:
        cur.execute(sql)

        # Check if there are any results
        entries = cur.fetchall()
        conn.close()
        if not entries:
            print('No entries')
            return
        return entries

    except Exception as e: 
        print(e)

# Get the programs that have at least one child enrolled in it
def getPopulatedPrograms():
    conn, cur = connectToDB()
    sql = """
        SELECT DISTINCT PID
        FROM ChildrenProgram
    """
    # Execute the query and close the connection
    try:
        cur.execute(sql)

        # Check if there are any results
        entries = cur.fetchall()
        conn.close()
        if not entries:
            print('No entries')
            return
        return entries

    except Exception as e: 
        print(e)

# Get all incident types
def getIncidentTypes():
    conn, cur = connectToDB()
    sql = """
        SELECT *
        FROM IncidentTypes
    """
    # Execute the query and close the connection
    try:
        cur.execute(sql)

        # Check if there are any results
        entries = cur.fetchall()
        conn.close()
        if not entries:
            print('No entries')
            return
        return entries

    except Exception as e: 
        print(e)

# Get means per month for children of a given Incident Type
def getMeansPerMonth(incident_type):
    conn, cur = connectToDB()
    sql = """
        SELECT count(distinct KID)
        FROM Incidents
        INNER JOIN IncidentClassification ON Incidents.IID = IncidentClassification.IID
        INNER JOIN IncidentTypes ON IncidentClassification.TID = IncidentTypes.TID
        WHERE M_In_Pgm = %s
        AND IncidentTypes.Name = '%s'
    """

    # Execute the query and close the connection
    try:
        total_children = countChildren()
        incident_type = str(incident_type)
        months = [str(i) for i in range(1,13)]
        means = []

        for month in months:
            query = sql % (month, incident_type)
            cur.execute(query)

            # Check if there are any results
            entries = cur.fetchall()
            if entries:
                means.append(round(float(entries[0][0]/total_children), 2))
        conn.close()

        mean = {'Mean Percentage of Youth':means}
        month = {'Month in Placement':months}

        return month, mean

    except Exception as e: 
        print(e)




def validateLogin(uname,pwd):
	conn, cur = connectToDB()
	sql = "SELECT * FROM Users WHERE username = '"+uname+"' AND password='"+pwd+"';"
	try:
		cur.execute(sql)	
		entries = cur.fetchall()
		conn.close()
		return entries
	except:
		conn.close()

#		
def getUserType(uname):
	conn, cur = connectToDB()
	sql = "SELECT UserType FROM Users WHERE username = '"+uname+"';"

	try:
		cur.execute(sql)
		entries = cur.fetchall()
		conn.close()
		return (entries[0][0])
	except:
		conn.close()

# Get the incident_type id given an incident name
def getTID(name):
    conn, cur = connectToDB()
    sql = """
        SELECT TID
        FROM IncidentTypes
        WHERE Name='%s'
    """
    # Stitch together the sql query
    sql = sql % (name)

    # Execute the query and close the connection
    try:
        cur.execute(sql)

        # Check if IncidentType exists
        entry = cur.fetchall()
        if not entry:
            conn.close()
            print('No entry')
            return
        else:
            conn.close()
            return entry[0][0]
    except Exception as e: 
        print(e)
        conn.close()
# Get latest id of the table last inserted to (serializable tables only)
def getLastID(id,table):
    conn, cur = connectToDB()
    sql = """
        SELECT MAX(%s) FROM %s;
    """
    sql = sql % (id, table)

    # Execute the query and close the connection
    try:
        cur.execute(sql)

        # Check if IncidentType exists
        entry = cur.fetchall()
        if not entry:
            conn.close()
            print('No entry')
            return
        else:
            conn.close()
            return entry[0][0]
    except Exception as e: 
        print(e)
        conn.close()

# Gets all entries from the User table
def getUsers():
	conn, cur = connectToDB()
	sql = "SELECT * FROM Users ORDER BY Last_Name;"
	
	try:
		cur.execute(sql)
		users = cur.fetchall()
		conn.close()
		return users
	except Exception as e:
		print(e)
		conn.close()
		
# Checks if the given username is already in the DB
def validateUsername(username):
	conn, cur = connectToDB()
	sql = "SELECT * FROM Users WHERE username='"+username+"';"
	
	try:
		cur.execute(sql)
		users = cur.fetchall()
		conn.close()
		if not users:
			return True
		else:
			return False
	except Exception as e:
		print(e)
		conn.close()

# Creates a new entry in the Users table with the given values
def createUser(values):
	conn, cur = connectToDB()
	sql = "INSERT INTO Users VALUES("
	for value in values:
		sql = sql + "'" + value + "',"
	
	sql = sql[:-1] + ");"

	try:
		cur.execute(sql)
		conn.commit()
		conn.close()
	except Exception as e:
		print(e)
		conn.close()
		
# Deletes a user from the Users table with the given UID
def removeUser(UID):
	conn, cur = connectToDB()
	sql = "DELETE FROM Users WHERE UID="+UID
	try:
		cur.execute(sql)
		conn.commit()
		conn.close()
	except Exception as e:
		print (e)
		conn.close()
		
# Changes the userType of the user with the given UID to the given userType
def changeUserType(UID,userType):
	conn, cur = connectToDB()
	sql = "UPDATE Users SET UserType = '"+userType+"' WHERE UID = "+UID+";"
	try:
		cur.execute(sql)
		conn.commit()
		conn.close()
	except Exception as e:
		print (e)
		conn.close()
	
# Changes the password of the user with the given UID to the given password
def changeUserPassword(UID,password):
	conn, cur = connectToDB()
	sql = "UPDATE Users SET Password = '"+password+"' WHERE UID = "+UID+";"
	try:
		cur.execute(sql)
		conn.commit()
		conn.close()
	except Exception as e:
		print (e)
		conn.close()
		

def storeReport(title,report):
    conn, cur = connectToDB()
    sql = f"""
        INSERT INTO Graph VALUES ('{title}',GETDATE(),'{report}')
    """
    try:
        print(sql)
        cur.execute(sql)
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        conn.close()

# Gets all of the saved report queries
def getSavedReports():
	conn, cur = connectToDB()
	sql = "SELECT * FROM Graph ORDER BY GID DESC"
	try:
		cur.execute(sql)
		entries = cur.fetchall()
		conn.close()
		return entries
	except Exception as e:
		print (e)
		conn.close()
		
# Deletes a report from the Graph table with the given GID
def removeReport(GID):
	conn, cur = connectToDB()
	sql = "DELETE FROM Graph WHERE GID="+GID
	try:
		print(sql)
		cur.execute(sql)
		conn.commit()
		conn.close()
	except Exception as e:
		print (e)
		conn.close()
		
# Verifies that the password meets CHP's requirements
def verifyPassword(pwd):
	# Requirement 1: Password must be between 8-25 characters
	if len(pwd) < 8:
		flash("Password must be at least 8 characters.","error")
	elif len(pwd) > 25:
		flash("Password must be no more than 25 characters.","error")
	
	# Requirement 2: Password must contain at least 1 letter, 1 number, and 1 symbol
	hasLetter = False
	hasNumber = False
	hasSymbol = False
	validSymbols = ["!","@","#","$","%","^","&","*","(",")","`","~","-","_","+","=","{","}","[","]",":",";","'","|","\"","<",",",">",".","?","/"]
	
	# Requirement 3: Password must not contain spaces
	hasSpace = False
	
	# Checking requirements 2 and 3
	for char in pwd:
		if char.isalpha():
			hasLetter = True
		elif char.isdigit():
			hasNumber = True
		elif char in validSymbols:
			hasSymbol = True
		elif " " in pwd:
			hasSpace = True
			
	# Check if any of the requirements failed and display the proper message(s)
	error = False
	
	if not hasLetter:
		flash("Password must contain at least one letter.","error")
		error = True
	if not hasNumber:
		flash("Password must contain at least one number.","error")
		error = True
	if not hasSymbol:
		flash("Password must contain at least one symbol.","error")
		error = True
	if hasSpace:
		flash("Password cannot contain spaces.","error")
		error = True
		
	# Return the opposite of error because this function should return true if the password is valid
	return not error
		
# Gets all Incident Reports	submitted by Donnamarie that have not been reviewed
def getUnreviewedReportsDM():
	conn, cur = connectToDB()
	sql = "SELECT * FROM Incidents WHERE Status = 'Not Reviewed' AND UID = (SELECT UID FROM Users WHERE Username='Donnamarie');"
	try:
		cur.execute(sql)
		entries = cur.fetchall()
		conn.close()
		return entries
	except Exception as e:
		print (e)
		conn.close()

# Gets all Incident Reports submitted by Interns (or anyone other than Donnamarie) that have not been reviewed
def getUnreviewedReportsInterns():
	conn, cur = connectToDB()
	sql = "SELECT * FROM Incidents WHERE Status = 'Not Reviewed' AND UID <> (SELECT UID FROM Users WHERE Username='Donnamarie');"
	try:
		cur.execute(sql)
		entries = cur.fetchall()
		conn.close()
		return entries
	except Exception as e:
		print (e)
		conn.close()		
		