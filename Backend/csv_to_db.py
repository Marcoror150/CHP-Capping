#!/usr/bin/env python3
from db_helper import *
import os
import re 


# Cleanse input from whitespace and commas
def cleanse(input):
    output = input.replace(' ', '')
    output = output.replace(',', '')
    output = output.replace('-', '')
    output = output.replace('\r', '')
    output = output.replace('\n', '')

    return output

# Cleanses elements in a list
def cleanseMany(input):
    for i, item in enumerate(input):
        input[i] = cleanse(item)
    return input

# Strip all characters that are not numbers or decimal
def cleanseNonNumbers(input):
    regex = re.compile(r'[^0-9^.,]')
    return regex.sub('', input)

# Parse data to be ready for insertion
def parseData(raw_data):
    data = []
    # Iterate the raw data to cleanse it, and parse out appropiate data types
    for i, item in enumerate(raw_data):
        raw_data[i] = cleanseNonNumbers(item)
        data_split = raw_data[i].split(',') 
        col1 = int(data_split[0])
        col2 = float(data_split[1])
        data.append([col1,col2])
    return data

# Converts all csv files into tables into the db
def main():
    os.chdir('csvs')
    files = os.listdir('.')

    # Loop through every csv file, create a table and insert data
    for file in files:
        if file.endswith('.csv'):
            f = open(file,'r')
            table = cleanse(f.readline().split(',')[0])
            columns = cleanseMany(f.readline().split(','))
            data = parseData(f.readlines())
            f.close()

            createTable(table,columns)
            insertTable(table,columns,data)
    
    showAllTables()    
if __name__ == "__main__":
    main()
