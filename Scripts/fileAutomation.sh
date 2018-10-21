#!/bin/bash
#
# Bash Script file used to automate the processing of info from incidents,
# then moving the processed files to an Archive folder.
# Author: Marc Christensen
###

RTC='./rtc'
YMP='./ymp'
SHP='./shp'
ABH='./abh'
GEFC='./gefc'

if [ -e $RTC ]
then
  echo "$RTC exists"
else
  echo "$RTC does not exist in this directory. Creating the directory now."
  mkdir $RTC
  cd $RTC
  mkdir Archive
  cd ../
fi

if [ -e $YMP ]
then
  echo "$YMP exists"
else
  echo "$YMP does not exist in this directory. Creating the directory now."
  mkdir $YMP
  cd $YMP
  mkdir Archive
  cd ../
fi

if [ -e $SHP ]
then
  echo "$SHP exists"
else
  echo "$SHP does not exist in this directory. Creating the directory now."
  mkdir $SHP
  cd $SHP
  mkdir Archive
  cd ../
fi

if [ -e $ABH ]
then
  echo "$ABH exists"
else
  echo "$ABH does not exist in this directory. Creating the directory now."
  mkdir $ABH
  cd $ABH
  mkdir Archive
  cd ../
fi

if [ -e $GEFC ]
then
  echo "$GEFC exists"
else
  echo "$GEFC does not exist in this directory. Creating the directory now."
  mkdir $GEFC
  cd $GEFC
  mkdir Archive
  cd ../
fi
