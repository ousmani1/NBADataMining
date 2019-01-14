#!/usr/bin/python

from urllib2 import urlopen
from bs4 import BeautifulSoup
import csv
import pandas as pd
import os
import time

start_time = time.time()

#### REALGM URLS ####
urlTeamMetrics = "https://basketball.realgm.com/nba/team-stats/2019/Advanced_Stats/Team_Totals/Regular_Season"

######################################
##### PULL TEAM METRICS FUNCTION #####
######################################

def createMetrics():
    page = urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    table = soup.find('table')
    rows = table.findAll('tr')

    outputWriter.writerow(
        ["Team", "TS%", "eFG%", "oREB%", "dREB%", "tREB%", "AST%", "TOV%", "STL%", "BLK%", "PPS", "oRAT", "dRAT", \
         "eDIF", "POS", "PACE"])

    for row in rows:
        data = row.find_all('td')
        for row in data:
            Team = str(data[1].get_text())
            TS = str('{0:.2f}'.format(float(data[2].get_text())))
            EF = str('{0:.2f}'.format(float(data[3].get_text())))
            oREB = str(data[5].get_text())
            dREB = str(data[6].get_text())
            tREB = str(data[7].get_text())
            AST = str(data[8].get_text())
            TOV = str(data[9].get_text())
            STL = str(data[10].get_text())
            BLK = str(data[11].get_text())
            PPS = str(data[12].get_text())
            oRAT = str(data[14].get_text())
            dRAT = str(data[15].get_text())
            eDIF = str(data[16].get_text())
            POS = str(data[17].get_text())
            PACE = str(data[18].get_text())

            outputWriter.writerow(
                [Team, TS, EF, oREB, dREB, tREB, AST, TOV, STL, BLK, PPS, oRAT, dRAT, eDIF, POS, PACE])

    outputFile.close()


################################################
##### PANDAS CLEANUP TEAM METRICS FUNCTION #####
################################################

def pandaCleanMetrics():
    inputFile = pd.read_csv(tempFile, encoding="ISO-8859-1", low_memory=False)
    df = pd.DataFrame(inputFile,
                      columns=["Team", "TS%", "eFG%", "oREB%", "dREB%", "tREB%", "AST%", "TOV%", "STL%", "BLK%", "PPS",
                               "oRAT", "dRAT", \
                               "eDIF", "POS", "PACE"])

    export = df.drop_duplicates()
    export.to_csv(exportFile)
    os.remove(tempFile)

    #### drop unnecessary first row ####
    fname_in = exportFile

    #### WHEN RUNNING FROM TERMINAL ####    
    fname_out = 'csv/teamMetrics.csv'

    ##fname_out = '../../resources/csv/TeamMetrics.csv'

    with open(fname_in, 'r') as fin, open(fname_out, 'w') as fout:
        reader = csv.reader(fin)
        writer = csv.writer(fout)
        for row in reader:
            writer.writerow(row[1:])

    os.remove(fname_in)

##### CREATE TEAM METRICS FILE #####
outputFile = open('rawdataTeam' + '.csv', 'w')
outputWriter = csv.writer(outputFile)

url = urlTeamMetrics
tempFile = 'rawdataTeam.csv'
exportFile = 'tempTeamMetrics.csv'

createMetrics()
pandaCleanMetrics()

print("--- %s seconds ---" % (time.time() - start_time))
