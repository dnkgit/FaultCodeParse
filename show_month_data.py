import sqlite3
from sqlite3 import Error
import os

import matplotlib as mpl
import matplotlib.pyplot as plt

class plotSqlResults():

    def __init__(self):
        pass

    def showTop20Totals(self, monthData):
        count = 0
        errorCode = []
        frequency = []
        print('')
        print(f"Top 20 for {monthData['Start']} to {monthData['End']}")
        print(f"Excluding faults: {monthData['Exclusions']}")
        print('')
        print('[Occurrences], [Error Code], [Error Description]')
        for item in monthData['Totals']:
            if count < 20:
                errorCode.append(item[0])
                frequency.append(item[2])
                print(f"[{item[2]}] [{item[0]}] [{item[1]}]")
            else:
                break
            count += 1

    def plotTop20Totals(self, monthData):
        count = 0
        errorCode = []
        frequency = []
        for item in monthData['Totals']:
            if count < 20:
                errorCode.append(item[0])
                frequency.append(item[2])
            else:
                break
            count += 1

        fix, ax = plt.subplots()
        # ax.bar(errorCode, frequency)
        bars=plt.bar(errorCode, height=frequency)
        plt.suptitle(f"Top 20 Error Codes from {monthData['Start']} to {monthData['End']}")
        plt.title(f"Excluding fault codes : {monthData['Exclusions']}")
        plt.xticks(rotation=90)
        plt.xlabel("Top 20 Fault Codes")
        plt.ylabel("Occurrences")
        plt.grid('both')
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x(), yval + .005, yval)
        plt.show()



class DoSqlQueries ():

    def __init__(self, os='Linux', startYear=2022, startMonth=6, endYear=2023, endMonth=9, exclusionList=""):
        self.__os = os
        self.__startYear = startYear
        self.__startMonth = startMonth
        self.__endYear = endYear
        self.__endMonth = endMonth
        self.__exclusionList = exclusionList
        self.query = ""

    ''' --------------- PUBLIC MEMBERS --------------------'''

    def returnDatabaseFilename(self):
        return self.__databaseFilename

    def setSqlQuery(self, newQuery):
        self.query = newQuery

    def doSqlAllTimeQuery(self):
        self.__configureYearQuery()
        return self.__doSqlQuery()

    def doSqlMonthlyQuery(self):
        self.__configureSqlQuery()
        return self.__doSqlQuery()

    def doSqlMonthlyResults(self):
        fullResult = []
       
        startYear = self.__startYear
        startMonth = self.__startMonth

        try:
            while self.__startYear <= self.__endYear:
                while self.__startMonth <= self.__endMonth:

                    dataDict = {}

                    print(f"Finding values for {self.__returnStartDate()} {self.__returnEndDate()}")
                    dataDict['Start'] = self.__returnStartDate()
                    dataDict['End'] = self.__returnEndDate()
                    dataDict['Exclusions'] = self.__exclusionList
                    dataDict['Totals'] = self.doSqlMonthlyQuery()
                    fullResult.append(dataDict)

                    self.__startMonth += 1

                self.__startMonth = 1
                self.__startYear += 1

        except Exception as e:
            print(f"Error in processing {e}")
            exit(1)

        finally:
            # restore values
            self.__startMonth = startMonth
            self.__startYear = startYear
            return fullResult

    ''' --------------- PRIVATE MEMBERS -------------------'''

    def __doSqlQuery(self):
        conn = sqlite3.connect(self.__getDatabaseFile())
        cursor = conn.cursor()
        cursor.execute(self.query)
        result = cursor.fetchall()
        conn.close()
        return result

    def __returnStartDate(self):
        return f'"{self.__startYear}-{self.__startMonth:02}-01"'

    def __returnEndDate(self):
        daysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        return f'"{self.__endYear}-{self.__startMonth:02}-{daysInMonth[self.__startMonth-1]:02}"'

    def __getDatabaseFile(self):
        if self.__os != 'Linux':
            basePath = r'C:\Work\Fault_Code_Analysis'
            dbFile = r'Maindb.db'
        else:
            basePath = r'/media/ka/51195D827A36E8AA/Dev/Dev/FaultCodes/'
            dbFile = r'MainDb.db'
        dbaseFile = os.path.join(basePath, dbFile)
        return dbaseFile
    
    def __configureSqlQuery(self):
        line1 = f'SELECT "ERROR_CODE", "ERROR_DESCRIPTION", Count("ERROR_CODE") '
        line2 = f'FROM machine_data WHERE "ActiveDateString" > {self.__returnStartDate()} AND "ActiveDateString" < {self.__returnEndDate()} '
        line3 = f'AND "ERROR_CODE" NOT IN ({exclusionList}) '
        line4 = f'GROUP BY "ERROR_CODE" '
        line5 = f'ORDER BY Count("ERROR_CODE") DESC;'
        self.query = line1+line2+line3+line4+line5

    def __configureYearQuery(self):
        line1 = f'SELECT "ERROR_CODE", "ERROR_DESCRIPTION", Count("ERROR_CODE") '
        line2 = f'FROM machine_data WHERE "ActiveDateString" > {self.__returnStartDate()} AND "ActiveDateString" < {self.__returnEndDate()} '
        line3 = f'AND "ERROR_CODE" NOT IN ({exclusionList}) '
        line4 = f'GROUP BY "ERROR_CODE" '
        line5 = f'ORDER BY Count("ERROR_CODE") DESC;'
        self.query = line1+line2+line3+line4+line5

    ''' --------------- END OF CLASS ---------------------'''

exclusionList = "'D0228', 'P1434'"
qr = DoSqlQueries(exclusionList=exclusionList, endYear=2023, endMonth=9)
results = qr.doSqlMonthlyResults()
allTime = qr.doSqlAllTimeQuery()

doPlot = plotSqlResults()
doPlot.showTop20Totals(allTime)
for monthData in results:
    doPlot.showTop20Totals(monthData)
    doPlot.plotTop20Totals(monthData)

