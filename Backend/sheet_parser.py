#!/usr/bin/env python3

# Main Python script parses the spreadsheet and inserts entries into tbe db
# Michael Gutierrez
# 10/16/2018

import os, re, calendar,subprocess
from pathlib import Path
from functions import cleanExcelFiles
from shutil import move
from parser_helper import *
from db_helper import insertTable
import pandas as pd

def parseFile(filename, program, incident_type,uid):
    csv_name = excel_to_csv(filename)
    csv_folder = Path("csvs/")

    csv_path = csv_folder / csv_name

    
    # os.chdir('./csvs/')
    # os.listdir()

    f = open(csv_path, 'r')
    lines = f.readlines()

    # Get the KID
    kid = getKID(lines)
    # print(kid)

    # Get Start Date
    start_date = getStartDate(lines)
    # print(start_date)

    # Get Incident Month Date
    incident_month = getMonthInProgram(lines,start_date)
    #print(incident_month)

    # Create list for child,child_program, and incident to be inserted to db
    child = [kid,None]
    child_program = [kid,program,start_date,None]

    # Insert statements
    #print('inserting child:', child)
    insertTable('Children',child)
    #print('inserting children program:', child_program)
    insertTable('ChildrenProgram',child_program)

    incident = [kid,incident_month,uid]
    #print('inserting incident:',incident)
    insertTable('Incidents',incident)

    # Get the Incident ID that was just created, and the type ID
    iid = getLastID('iid','Incidents')
    tid = int(getTID(incident_type))

    # Create a list for the classsification to be inserted
    incident_classification = [iid,tid]
    #print('inserting incident classification:', incident_classification)
    insertTable('IncidentClassification',incident_classification)
    #print('done...')
   
    # Destination path of the already parsed file
    destination = Path(f'csvs/{program}/archive/{csv_name}')
    try:
        # Move the file
        if os.path.exists( Path(f'csvs/{program}/archive/')):
            move(csv_path,destination)
        else:
            status_code = subprocess.call("md csvs\\RTC\\archive csvs\\YMP\\archive csvs\\SHP\\archive csvs\\ABH\\archive  csvs\\GEFC\\archive", shell=True) 
            if status_code is 0:
                move(csv_path,destination) 
    except Exception as e:
        print(e,"...")
        # status_code = subprocess.call("md csvs\\RTC\\archive csvs\\YMP\\archive csvs\\SHP\\archive csvs\\ABH\\archive  csvs\\GEFC\\archive", shell=True) 
        # if status_code is 0:
        #     move(csv_path,destination) 
    f.close()
    try:
        os.remove(csv_path)
    except Exception as e:
        print(e)  


# Function to convert an excel sheet to csv format
def excel_to_csv(filename):
    # Get a filename from the excel filename
    file = filename.split('.')
    
    # Return the filename if it's already a csv
    if file[1] == 'csv':
        return filename

    # Make a new filename with csv extension
    csv_name = f'{file[0]}.csv'

    # Directory where uploaded files reside
    csv_folder = Path("csvs/")

    # Path of the uploaded file
    excel_file = csv_folder / filename

    # Path of the new csv being created
    csv_file = csv_folder / csv_name

    # Convert to csv format and write the file to the directory
    data_xls = pd.read_excel(excel_file, index_col=None)
    data_xls.to_csv(csv_file, encoding='utf-8')
    cleanExcelFiles()

    # Return the csv name
    return csv_name


