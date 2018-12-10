#!/usr/bin/env python3

# Additional functions used by the parser script.
# Michael Gutierrez
# 10/31/2018
import re
from datetime import datetime
from dateutil import relativedelta
from db_helper import getTID,getLastID

    
def getKID(lines):
    # Regex to find the kid
    regex = r'#([0-9]*)'

    # Iterate through the file lines
    for line in lines:

        # Search the line for a regex match
        match = re.search(regex,line)

        # Return the matched string if there is one
        if match:
            return int(match.group(1))
    else:
        return None

def getStartDate(lines):
    # Regex to find the line where the start date resides
    line_regex = r'Admitted:'

    # Regex to parse out the start date
    date_regex = r'\d+/\d+/\d+'

    # Iterate through the file lines
    for line in lines:

        # Search the line for a regex match
        match = re.search(line_regex, line, re.IGNORECASE)
    
        # Return a matched date string
        if match:
            return re.search(date_regex, line).group()

    # If can't find the start date, try a different regex
    else:
        # Different regex to help find the line where the start date resides
        line_regex = r'Placement Date'

        # Regex to parse out the start date
        date_regex = r'\d+-\d+-\d+'

        # Iterate through the file lines
        for i,line in enumerate(lines):

            # Search the line for a regex match
            match = re.search(line_regex, line, re.IGNORECASE)
        
            # Return the start date which resides one line ahead
            if match:
                date_string =  re.search(date_regex, lines[i+1]).group()
                
                # Return the correct string date
                return str(datetime.strptime(date_string, '%Y-%m-%d').strftime('%m/%d/%Y'))
        else:
            return None

# Function to parse out the incident
def getIncidentDate(lines):
    # Regex to find the line where the start date resides
    line_regex = r'Time '

    # Regex to parse out the start date
    date_regex = r'\d+/\d+/\d+'

    # Iterate through the file lines
    for line in lines:

        # Search the line for a regex match
        match = re.search(line_regex, line, re.IGNORECASE)
    
        # Return a matched date string
        if match:
            return re.search(date_regex, line).group()

    # If can't find the start date, try a different regex
    else:
        # Different regex to help find the line where the start date resides
        line_regex = r'Date'

        # Regex to parse out the start date
        date_regex = r'\d+/\d+/\d+'

        # Iterate through the file lines
        for i,line in enumerate(lines):

            # Search the line for a regex match
            match = re.search(line_regex, line, re.IGNORECASE)
        
            # Return the start date which resides one line ahead
            if match:
                return re.search(date_regex, lines[i+1]).group()
        else:
            return None

# Function to calculate the month a child was involved with an incident
def getMonthInProgram(lines,start_date):
    # Get the incident date
    incident_date = getIncidentDate(lines)

    # Convert dates to a date object
    start_date = datetime.strptime(start_date, '%m/%d/%Y')
    incident_date = datetime.strptime(incident_date, '%m/%d/%Y')

    # Calculate the month in the program that incident occured
    month = relativedelta.relativedelta(incident_date, start_date).months
    return month

def getIncidentType(lines):
    pass




