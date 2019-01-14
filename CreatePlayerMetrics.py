#!/usr/bin/python

from urllib2 import urlopen
from bs4 import BeautifulSoup
import csv
import pandas as pd
import os
import time

start_time = time.time()

#### REALGM URLS ####
urlPlayersMetrics1 = "https://basketball.realgm.com/nba/stats/2019/Advanced_Stats/Qualified/points/All/desc/1/Regular_Season"
urlPlayersMetrics2 = "https://basketball.realgm.com/nba/stats/2019/Advanced_Stats/Qualified/per/All/desc/2/Regular_Season"
urlPlayersMetrics3 = "https://basketball.realgm.com/nba/stats/2019/Advanced_Stats/Qualified/per/All/desc/3/Regular_Season"
urlPlayersMetrics4 = "https://basketball.realgm.com/nba/stats/2019/Advanced_Stats/Qualified/per/All/desc/4/Regular_Season"

########################################
##### PULL PLAYER METRICS FUNCTION #####
########################################

def createPlayerMetrics():
    page = urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    table = soup.find('table')
    rows = table.findAll('tr')

    if count < 1:
        outputWriter.writerow(
            ["Player", "Team", "TS%", "eFG%", "oREB%", "dREB%", "tREB%", "AST%", "TOV%", "STL%", "BLK%", "USG%", "PPS", \
            "oRAT", "dRAT", "eDIF", "PER"])

    for row in rows:
        data = row.find_all('td')
        for row in data:
            Player = str(data[1].get_text())
            Team = str(data[2].get_text())
            TS = str('{0:.2f}'.format(float(data[3].get_text())))
            EF = str('{0:.2f}'.format(float(data[4].get_text())))
            oREB = str(data[6].get_text())
            dREB = str(data[7].get_text())
            tREB = str(data[8].get_text())
            AST = str(data[9].get_text())
            TOV = str(data[10].get_text())
            STL = str(data[11].get_text())
            BLK = str(data[12].get_text())
            USG = str(data[13].get_text())
            PPS = str(data[15].get_text())
            oRAT = str(data[16].get_text())
            dRAT = str(data[17].get_text())
            eDIF = str(data[18].get_text())
            PER = str(data[20].get_text())

            outputWriter.writerow(
                [Player, Team, TS, EF, oREB, dREB, tREB, AST, TOV, STL, BLK, USG, PPS, oRAT, dRAT, eDIF, PER])


##################################################
##### PANDAS CLEANUP PLAYER METRICS FUNCTION #####
##################################################

def pandaCleanPlayerMetrics():
    inputFile = pd.read_csv(tempFile, encoding="ISO-8859-1", low_memory=False)
    df = pd.DataFrame(inputFile,
                      columns=["Player", "Team", "TS%", "eFG%", "oREB%", "dREB%", "tREB%", "AST%", "TOV%", "STL%",
                               "BLK%", "USG%", "PPS", "oRAT", "dRAT", \
                               "eDIF", "PER"])

    export = df.drop_duplicates()
    export.to_csv(exportFile)
    os.remove(tempFile)

    #### drop unnecessary first column ####
    fname_in = exportFile

    #### WHEN RUNNING FROM TERMINAL ####        
    fname_out = 'csv/playerMetrics.csv'

    ##fname_out = '../../resources/csv/PlayerMetrics.csv'

    with open(fname_in, 'r') as fin, open(fname_out, 'w') as fout:
        reader = csv.reader(fin)
        writer = csv.writer(fout)
        for row in reader:
            writer.writerow(row[1:])

    os.remove(fname_in)


##### CREATE PLAYER METRIC FILES #####

outputFile = open('rawdataPlay' + '.csv', 'w')
outputWriter = csv.writer(outputFile)

urlList = [urlPlayersMetrics1, urlPlayersMetrics2, urlPlayersMetrics3, urlPlayersMetrics4]
tempFile = 'rawdataPlay.csv'
exportFile = 'tempPlayerMetrics.csv'

count = 0
for url in urlList:
    createPlayerMetrics()
    count += 1

outputFile.close()
pandaCleanPlayerMetrics()

print("--- %s seconds ---" % (time.time() - start_time))
