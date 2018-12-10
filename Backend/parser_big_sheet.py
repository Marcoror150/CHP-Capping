#!/usr/bin/env python3

# Main Python script parses the spreadsheet and inserts entries into tbe db
# Michael Gutierrez
# 10/16/2018

import os, re, calendar
from db_helper import *

def parseBigSheet(file,program):

    # Open the correct csv and chose the right program
    # TODO: automate this
    f = open(file, 'r')

    # Header line of the csv
    header = f.readline().split(',')
    incidents_types = header[4:16]
    
    # Iterate over every entry in the csv and parse out the columns of data
    for i,line in enumerate(f.readlines()):
        child_info = line.split(',')

        # KID, Start Date, and ACEs Score
        KID = int(child_info[0])
        # KID = child_info[0]

        start_date = child_info[1]
        try:
            end_date = child_info[2]
        except IndexError:
            end_date = None

        try:
            ACEs_score = int(child_info[3])
        except:
            ACEs_score = None
    
        # Insert the child if they already doesn't exist and their program info
        child = []
        child_programs = []
        child.extend((KID,ACEs_score))
        child_programs.extend((KID,program,start_date,end_date))


        # insertTable('Children',child)
        # insertTable('ChildrenProgram',child_programs)

        # Seperate out the incident data
        incidents = child_info[4:]

        # Counter to keep track of what column is currently being parsed 
        counter = 0

        # Variable to track if there is an incident that needs to be inserted
        need_insert = False 

        # Variable to track the month is being looked at
        month = None

        # Variable to temporarily store incident id
        iid = ''

        # Loop incident columns in one entry
        for idx,val in enumerate(incidents):
            try:
                val = int(val)
            except:
                # print('Child left')
                break

            if counter == 0:
                month = int(val)
                # print('\n',incidents_types[counter],':', month)
                counter+=1

            elif counter == 1:
                phys_ass = val
                # print(incidents_types[counter],':',phys_ass)
                if phys_ass != 0:
                    # print('inserting',incidents_types[counter])
                    need_insert = True
                counter+=1

            elif counter == 2:
                sex_agg = val
                # print(incidents_types[counter],':',sex_agg)
                if sex_agg != 0:
                    # print('inserting',incidents_types[counter])
                    need_insert = True
                counter+=1

            elif counter == 3:
                restraints = val
                # print(incidents_types[counter],':',restraints)
                if restraints != 0:
                    # print('inserting',incidents_types[counter])
                    need_insert = True
                counter+=1

            elif counter == 4:
                awols = val
                # print(incidents_types[counter],':',awols)
                if awols != 0:
                    # print('inserting',incidents_types[counter])
                    need_insert = True
                counter+=1

            elif counter == 5:
                self_harm = val
                # print(incidents_types[counter],':',self_harm)
                if self_harm != 0:
                    # print('inserting',incidents_types[counter])
                    need_insert = True
                counter+=1

            elif counter == 6:
                prop_dam = val
                # print(incidents_types[counter],':',prop_dam)
                if sex_agg != 0:
                    # print('inserting',incidents_types[counter])
                    need_insert = True
                counter+=1

            elif counter == 7:
                steal = val
                # print(incidents_types[counter],':',steal)
                if steal != 0:
                    # print('inserting',incidents_types[counter])
                    need_insert = True
                counter+=1

            elif counter == 8:
                weapons = val
                # print(incidents_types[counter],':',weapons)
                if weapons != 0:
                    # print('inserting',incidents_types[counter])
                    need_insert = True
                counter+=1
                
            elif counter == 9:
                suicide = val
                # print(incidents_types[counter],':',suicide)
                if suicide != 0:
                    # print('inserting',incidents_types[counter])
                    need_insert = True
                counter+=1

            elif counter == 10:
                er_visits = val
                # print(incidents_types[counter],':',er_visits)
                if er_visits != 0:
                    # print('inserting',incidents_types[counter])
                    need_insert = True
                counter+=1

            elif counter == 11:
                month_total = val
                # print(incidents_types[counter],'in month', str(month) , ':',str(month_total))
                counter = 0
                need_insert = False

            if need_insert:
                incident = []
                incident.extend((KID,month))
                insertTable('Incidents',incident)
                iid = getLastID('iid','Incidents')

                incident_class = []
                tid = int(getTID(incidents_types[counter-1]))

                incident_class.extend((iid,tid))

                insertTable('IncidentClassification',incident_class)
                need_insert = False

        f.close()
        # Testing purposes
        # print('only 1 child')
        
