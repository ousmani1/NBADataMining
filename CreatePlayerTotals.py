#!/usr/bin/python

from urllib2 import urlopen
from bs4 import BeautifulSoup
import csv
import pandas as pd
import os
import time

start_time = time.time()

#### REALGM URL ####
urlPlayersTotals1 = "https://basketball.realgm.com/nba/stats/2019/Totals/Qualified/points/All/desc/1/Regular_Season"
urlPlayersTotals2 = "https://basketball.realgm.com/nba/stats/2019/Totals/Qualified/points/All/desc/2/Regular_Season"
urlPlayersTotals3 = "https://basketball.realgm.com/nba/stats/2019/Totals/Qualified/points/All/desc/3/Regular_Season"

#####################################
##### PULL PLAYER DATA FUNCTION #####
#####################################

def createPlayerData():
    page = urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    table = soup.find('table')
    rows = table.findAll('tr')

    if count < 1:
        outputWriter.writerow(["Player", "Team", "GP", "MIN", "FGM", "FGA", "FG%", "3PM", "3PA", "3P%", "FTM", "FTA", "FT%", \
                           "TOV", "PFS", "ORB", "DRB", "REB", "AST", "STL", "BLK", "PTS"])

    for row in rows:
        data = row.find_all('td')
        for row in data:
            Player = str(data[1].get_text())
            Team = str(data[2].get_text())
            GP = str(data[3].get_text())
            MIN = str(data[4].get_text())
            FGM = str(data[5].get_text())
            FGA = str(data[6].get_text())
            FGP = str('{0:.2f}'.format(float(data[7].get_text())))
            TPM = str(data[8].get_text())
            TPA = str(data[9].get_text())
            TPP = str('{0:.2f}'.format(float(data[10].get_text())))
            FTM = str(data[11].get_text())
            FTA = str(data[12].get_text())
            FTP = str('{0:.2f}'.format(float(data[13].get_text())))
            TOV = str(data[14].get_text())
            PFS = str(data[15].get_text())
            ORB = str(data[16].get_text())
            DRB = str(data[17].get_text())
            REB = str(data[18].get_text())
            AST = str(data[19].get_text())
            STL = str(data[20].get_text())
            BLK = str(data[21].get_text())
            PTS = str(data[22].get_text())

            outputWriter.writerow(
                [Player, Team, GP, MIN, FGM, FGA, FGP, TPM, TPA, TPP, FTM, FTA, FTP, TOV, PFS, ORB, DRB, \
                 REB, AST, STL, BLK, PTS])

def pandaCleanPlayerData():
    inputFile = pd.read_csv(tempFile, encoding="ISO-8859-1", low_memory=False)
    df = pd.DataFrame(inputFile,
                      columns=["Player", "Team", "GP", "MIN", "FGM", "FGA", "FG%", "3PM", "3PA", "3P%", "FTM", "FTA",
                               "FT%", \
                               "TOV", "PFS", "ORB", "DRB", "REB", "AST", "STL", "BLK", "PTS"])

    export = df.drop_duplicates()
    export.to_csv(exportFile)
    os.remove(tempFile)

    #### drop unnecessary first column ####
    fname_in = exportFile

    #### WHEN RUNNING FROM TERMINAL ####    
    fname_out = 'csv/playerTotals.csv'

    #fname_out = '../../resources/csv/PlayerTotals.csv'

    with open(fname_in, 'r') as fin, open(fname_out, 'w') as fout:
        reader = csv.reader(fin)
        writer = csv.writer(fout)
        for row in reader:
            writer.writerow(row[1:])

    os.remove(fname_in)

##### CREATE PLAYER AVERAGES FILES #####

outputFile = open('rawdataPlay' + '.csv', 'w')
outputWriter = csv.writer(outputFile)

urlList = [urlPlayersTotals1, urlPlayersTotals2, urlPlayersTotals3]
tempFile = 'rawdataPlay.csv'
exportFile = 'tempPlayerTotals.csv'

count = 0
for url in urlList:
    createPlayerData()
    count += 1

outputFile.close()
pandaCleanPlayerData()

print("--- %s seconds ---" % (time.time() - start_time))
