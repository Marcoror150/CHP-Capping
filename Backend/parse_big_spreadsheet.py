#!/usr/bin/env python3
import os
import re
import calendar
from db_helper import *

def main():
    os.chdir('./../csvs')  
    f = open('BIR Study- On Campus Residential - Better.csv', 'r')
    program = 'RES'
    header = f.readline().split(',')
    incedents_types = header[4:16]
    print(incedents_types)
    
    for line in f.readlines():
        child_info = line.split(',')
        name = child_info[0].split(' ')[1]
        date_entry = child_info[1]
        date_departure = child_info[2]
        ace_score = child_info[3]

        incedents = child_info[4:]
        
        print(name)
        counter = 0
        for idx,val in enumerate(incedents):
            if counter == 0:
                month = val
                print(incedents_types[counter]+':'+month)
                counter+=1
            elif counter == 1:
                phys_ass = val
                # print(incedents_types[counter]+':'+phys_ass)
                counter+=1
            elif counter == 2:
                sex_agg = val
                # print(incedents_types[counter]+':'+sex_agg)
                counter+=1
            elif counter == 3:
                restraints = val
                # print(incedents_types[counter]+':'+restraints)
                counter+=1
            elif counter == 4:
                awols = val
                # print(incedents_types[counter]+':'+awols)
                counter+=1
            elif counter == 5:
                self_harm = val
                # print(incedents_types[counter]+':'+self_harm)
                counter+=1
            elif counter == 6:
                prop_dam = val
                # print(incedents_types[counter]+':'+prop_dam)
                counter+=1
            elif counter == 7:
                steal = val
                # print(incedents_types[counter]+':'+steal)
                counter+=1
            elif counter == 8:
                weapons = val
                # print(incedents_types[counter]+':'+weapons)
                counter+=1
            elif counter == 9:
                suicide = val
                # print(incedents_types[counter]+':'+suicide)
                counter+=1
            elif counter == 10:
                er_visits = val
                # print(incedents_types[counter]+':'+er_visits)
                counter+=1
            elif counter == 11:
                month_total = val
                print(incedents_types[counter]+':'+month_total)
                counter = 0

        print('only 1 child')
        break
        # print(header[0] + ':'+ name)
        # print(header[1] + ':'+ date_entry)
        # print(header[2] + ':'+ date_departure)
        # print(header[3] + ':'+ ace_score)
        # print(month + '\n')





        # for x in child_info:
        #     print(x)

if __name__ == "__main__":
    main()
