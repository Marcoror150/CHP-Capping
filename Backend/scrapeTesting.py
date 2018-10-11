from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
import os

os.system('../../PdfTesting/pdfminer-master/tools/pdf2txt.py -o test.txt BIRSample.pdf')
file = open("test.txt","r")
temp = file.readlines()
print temp[45:55]
line = temp[3]
cid = 0
for i, s in enumerate(line):
    if s == "#":
        cid = line[i+1:-2]
        break

print "CID: "+cid

program = temp[19].rstrip()
print "Program: "+program

dateOfAdmiss = temp[21].rstrip()
print "Date of Admission: "

date = temp[25][18:].rstrip()
print "Incident Date: "+date

desc = temp [49][10:].rstrip()
print "Description: "+desc

incidentTypes = temp[50][17:].rstrip().split(", ")
print "Incident Types: "
print (", ".join(incidentTypes))
