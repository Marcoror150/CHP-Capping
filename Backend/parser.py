#!/usr/bin/env python3

# Main Python script parses data from csvs to be inserted into the db
# Michael Gutierrez
# 10/16/2018

import os, re, calendar
from db_helper import *
from parser_helper import *

def main():

    csv = open('../csvs/13870-Detailed.csv', 'r', encoding="utf8", errors='ignore')
    kid = getKID(csv)
    

if __name__ == "__main__":
    main()
