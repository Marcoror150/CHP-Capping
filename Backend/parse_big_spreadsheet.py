#!/usr/bin/env python3

# Main Python script parses the spreadsheet and inserts entries into tbe db
# Michael Gutierrez
# 10/16/2018

import os
import re
import calendar
from db_helper import *

def main():

    # Open the correct csv and chose the right program
    # TODO: automate this
    os.chdir('./../csvs')  
    f = open('CHP-RES - RTC Data.csv', 'r')
    program = 'RES'

    # Header line of the csv
    header = f.readline().split(',')
    incidents_types = header[4:16]
    
    # Iterate over every entry in the csv and parse out the columns of data
    for line in f.readlines():
        child_info = line.split(',')

        # KID, Start Date, and ACEs Score
        KID = int(child_info[0])
        start_date = child_info[1]
        print('Child: ' + str(KID))
        try:
            end_date = child_info[2]
        except IndexError:
            end_date = None

        try:
            ACEs_score = child_info[3]
        except IndexError:
            ACESs_score = None
    
        # Insert the child if they already doesn't exist and their program info
        # insertTable('Children',[KID,ACEs_score])
        # insertTable('ChildrenPrograms',[KID,program,start_date,end_date])

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
            if counter == 0:
                month = int(val)
                print('\n'+incidents_types[counter]+':'+ str(month))
                counter+=1

            elif counter == 1:
                phys_ass = val
                print(incidents_types[counter]+':'+phys_ass)
                if phys_ass == '':
                    need_insert = False
                else:
                    need_insert = True
                counter+=1

            elif counter == 2:
                sex_agg = val
                print(incidents_types[counter]+':'+sex_agg)
                if sex_agg == '':
                    need_insert = False
                else:
                    need_insert = True
                counter+=1

            elif counter == 3:
                restraints = val
                print(incidents_types[counter]+':'+restraints)
                if restraints == '':
                    need_insert = False
                else:
                    need_insert = True
                counter+=1

            elif counter == 4:
                awols = val
                print(incidents_types[counter]+':'+awols)
                if awols == '':
                    need_insert = False
                else:
                    need_insert = True
                counter+=1

            elif counter == 5:
                self_harm = val
                print(incidents_types[counter]+':'+self_harm)
                if self_harm == '':
                    need_insert = False
                else:
                    need_insert = True
                counter+=1

            elif counter == 6:
                prop_dam = val
                print(incidents_types[counter]+':'+prop_dam)
                if sex_agg == '':
                    prop_dam = False
                else:
                    need_insert = True
                counter+=1

            elif counter == 7:
                steal = val
                print(incidents_types[counter]+':'+steal)
                if steal == '':
                    need_insert = False
                else:
                    need_insert = True
                counter+=1

            elif counter == 8:
                weapons = val
                print(incidents_types[counter]+':'+weapons)
                if weapons == '':
                    need_insert = False
                else:
                    need_insert = True
                counter+=1
                
            elif counter == 9:
                suicide = val
                print(incidents_types[counter]+':'+suicide)
                if suicide == '':
                    need_insert = False
                else:
                    need_insert = True
                counter+=1

            elif counter == 10:
                er_visits = val
                print(incidents_types[counter]+':'+er_visits)
                if er_visits == '':
                    need_insert = False
                else:
                    need_insert = True
                counter+=1

            elif counter == 11:
                month_total = val
                print(incidents_types[counter]+':'+month_total)
                counter = 0
                need_insert = False
            
            # if need_insert:
            #     insertTable('Incidents',[KID,month])
            #     iid = getLastID()
            #     tid = getTID(incidents_types[counter])
            #     insertTable('IncidentClassification',[iid,tid])

        # Testing purposes
        # print(month)
        # print('only 1 child')
        # break

if __name__ == "__main__":
    main()
