#!/usr/bin/python

from urllib2 import urlopen
from bs4 import BeautifulSoup
import csv
import pandas as pd
import os
import time

start_time = time.time()

#### RealGM URL ####
urlOppoAverages = "https://basketball.realgm.com/nba/team-stats/2019/Averages/Opponent_Totals/Regular_Season"


###################################
##### PULL TEAM DATA FUNCTION #####
###################################

def createData():
    page = urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    table = soup.find('table')
    rows = table.findAll('tr')

    outputWriter.writerow(["Team", "GP", "MIN", "FGM", "FGA", "FG%", "3PM", "3PA", "3P%", "FTM", "FTA", "FT%", \
                           "TOV", "PFS", "ORB", "DRB", "REB", "AST", "STL", "BLK", "PTS"])

    for row in rows:
        data = row.find_all('td')
        for row in data:
            Team = str(data[1].get_text())
            GP = str(data[2].get_text())
            MIN = str(data[3].get_text())
            FGM = str(data[4].get_text())
            FGA = str(data[5].get_text())
            FGP = str('{0:.2f}'.format(float(data[6].get_text())))
            TPM = str(data[7].get_text())
            TPA = str(data[8].get_text())
            TPP = str('{0:.2f}'.format(float(data[9].get_text())))
            FTM = str(data[10].get_text())
            FTA = str(data[11].get_text())
            FTP = str('{0:.2f}'.format(float(data[12].get_text())))
            TOV = str(data[13].get_text())
            PFS = str(data[14].get_text())
            ORB = str(data[15].get_text())
            DRB = str(data[16].get_text())
            REB = str(data[17].get_text())
            AST = str(data[18].get_text())
            STL = str(data[19].get_text())
            BLK = str(data[20].get_text())
            PTS = str(data[21].get_text())

            outputWriter.writerow([Team, GP, MIN, FGM, FGA, FGP, TPM, TPA, TPP, FTM, FTA, FTP, TOV, PFS, ORB, DRB, \
                                   REB, AST, STL, BLK, PTS])
    outputFile.close()

##############################################
##### PANDAS CLEANUP TEAM DATA FUNCTION #####
##############################################

def pandaClean():
    inputFile = pd.read_csv(tempFile, encoding="ISO-8859-1", low_memory=False)
    df = pd.DataFrame(inputFile,
                      columns=["Team", "GP", "MIN", "FGM", "FGA", "FG%", "3PM", "3PA", "3P%", "FTM", "FTA", "FT%", \
                               "TOV", "PFS", "ORB", "DRB", "REB", "AST", "STL", "BLK", "PTS"])

    export = df.drop_duplicates()
    export.to_csv(exportFile)
    os.remove(tempFile)

    #### drop unnecessary first row ####
    fname_in = exportFile
    
    #### WHEN RUNNING FROM TERMINAL ####    
    fname_out = 'csv/oppoAverages.csv'
    
    #fname_out = '../../resources/csv/OpponentAverages.csv'

    with open(fname_in, 'r') as fin, open(fname_out, 'w') as fout:
        reader = csv.reader(fin)
        writer = csv.writer(fout)
        for row in reader:
            writer.writerow(row[1:])

    os.remove(fname_in)

##### CREATE OPPONENT AVERAGES FILE #####

outputFile = open('rawdataOppo' + '.csv', 'w')
outputWriter = csv.writer(outputFile)

url = urlOppoAverages
tempFile = 'rawdataOppo.csv'
exportFile = 'tempOppoAverages.csv'

createData()
pandaClean()

print("--- %s seconds ---" % (time.time() - start_time))
