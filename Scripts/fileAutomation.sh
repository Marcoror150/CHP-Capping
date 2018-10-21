#!/bin/bash
#
# Bash Script file used to automate the processing of info from incidents,
# then moving the processed files to an Archive folder.
# Author: Marc Christensen
###

RTC='./rtc'
YMP='./ymp'
SHP='.shp'
ABH='./abh'
GEFC='./gefc'

if [ -e $RTC ]
then
  echo "$RTC exists"
else
  echo "$RTC does not exist in this directory. Creating the directory now."
  mkdir $RTC
fi

