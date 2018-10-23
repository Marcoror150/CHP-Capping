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

#Create any directories that are missing below the current directory
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

#Set variables to all files within each directory
RTCFiles=`ls ./rtc`
YMPFiles=`ls ./ymp`
SHPFiles=`ls ./shp`
ABHFiles=`ls ./abh`
GEFCFiles=`ls ./gefc`

#Convert all .xlsx files to .csv files for further processing
for file in $RTCFiles
do
if [ ${file:-5} ==".xlsx" ] #get any Excel file
then	
  mv $RTC/$file

#Execute parsing of.csv files and move them to Archive if successed for RTC
for file in $RTCFiles
do
if [ ${file: -4} == ".csv" ] #get any file that ends in .csv
then
  sh
  ../reportParsing.sh $RTC/$file
  EXITCODE=$?
  if [ $EXITCODE -eq 0 ] #If the script had no issues
    then
    mv $RTC/$file $RTC/Archive #Move to respective archive
  fi
fi
done

#Execute parsing of.csv files and move them to Archive if successed for YMP
for file in $YMPFiles
do
if [ ${file: -4} == ".csv" ] #get any file that ends in .csv
then
  sh ../reportParsing.sh $YMP/$file
  EXITCODE=$?
  if [ $EXITCODE -eq 0 ] #If the script had no issues
    then
    mv $YMP/$file $YMP/Archive #Move to respective archive
  fi
fi
done

#Execute parsing of.csv files and move them to Archive if successed for SHP
for file in $SHPFiles
do
if [ ${file: -4} == ".csv" ] #get any file that ends in .csv
then
  sh ../reportParsing.sh $SHP/$file
  EXITCODE=$?
  if [ $EXITCODE -eq 0 ] #If the script had no issues
    then
    mv $SHP/$file $SHP/Archive #Move to respective archive
  fi
fi
done

#Execute parsing of.csv files and move them to Archive if successed for ABH
for file in $ABHFiles
do
if [ ${file: -4} == ".csv" ] #get any file that ends in .csv
then
  sh ../reportParsing.sh $ABH/$file
  EXITCODE=$?
  if [ $EXITCODE -eq 0 ] #If the script had no issues
    then
    mv $ABH/$file $ABH/Archive #Move to respective archive
  fi
fi
done

#Execute parsing of.csv files and move them to Archive if successed for GEFC
for file in $GEFCFiles
do
if [ ${file: -4} == ".csv" ] #get any file that ends in .csv
then
  sh ../reportParsing.sh $GEFC/$file
  EXITCODE=$?
  if [ $EXITCODE -eq 0 ] #If the script had no issues
    then
    mv $GEFC/$file $GEFC/Archive #Move to respective archive
  fi
fi
done
