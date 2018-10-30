#!/usr/bin/env python3
import re
def cleanEmptyRows(csv):
    regex = re.compile(r'^(,)*$')
    csv = csv.readlines()[2:-14]
    return [line for line in csv if not regex.match(line)]
def getKID(csv):
    regex = re.compile(r'#[0-9]*')
    for i in csv:
        if not regex.match(i):
            print(i)
