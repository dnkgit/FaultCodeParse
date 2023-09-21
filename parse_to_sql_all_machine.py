import pandas as pd
import sqlite3
from sqlite3 import Error
import os
import datetime

activatedColumnName = 'Activated Time'
clearedColumnName = 'Cleared Time'
# test format useColumns = ['VIN','Name','Machine Profile','MachineHours','Severity','Severity Description','DTC Code','SPN','FMI','Source Address (Decimal)','Source Address (Hexadecimal)',activatedColumnName,clearedColumnName,'Error Code','Error Code Description','Script action(s)']
# test format removeColumns = ['Name', 'Machine Profile', 'Severity Description', 'DTC Code', 'Source Address (Decimal)', 'Script action(s)']
useColumns = ['VIN','MACHINE_ID','DTC','SPN','FMI','SRCADDR_DEC','SRCADDR_HEX','ERROR_CODE','ERROR_DESCRIPTION','SEVERITY',activatedColumnName,clearedColumnName]
removeColumns = ['MACHINE_ID', 'DTC', 'SRCADDR_DEC']

def removeLineEndings(stringIn):
    stringOut = stringIn.replace('\n', '')
    stringOut = stringOut.replace('\r', '')
    return stringOut

def getTimestamp():
    return datetime.datetime.now()

def updateProcessedList(fileName, info):
    
    info = removeLineEndings(info)
    try:
        f = open(fileName, 'a')
        f.write(f"{getTimestamp()} - {info}\n")
    except Exception as e:
        print(f"Cannot open or update file {fileName} {e}")
    finally:
        try:
            f.close()
        finally:
            pass

def convertTimestampsToNewCols(dateColName, timeColname, column, dataFrame):
    DateList = []
    TimeList = []

    # print(column)

    for timestring in column:
        tString = str(timestring)
        if len(tString) == len("2021-09-05 11:16:00"):
            DateList.append(tString[:10])
            TimeList.append(tString[-8:])
        else:
            DateList.append("2000-01-01")
            TimeList.append("00:00:00")

    dataFrame[dateColName] = DateList
    dataFrame[timeColname] = TimeList

def tidyDataFrame(dataFrame):
    global removeColumns
    for name in removeColumns:
        if name in dataFrame.columns:
            del dataFrame[name]

def ProcessFileToSql(inputFile, dbFile, reportFile):
    global activatedColumnName
    global clearedColumnName
    global useColumns
    
    inputFile = removeLineEndings(inputFile)

    continueProcessing = True
    
    if continueProcessing:
        try:
            xls = pd.ExcelFile(inputFile)
            df_machine_data = pd.read_excel(xls, 'ALL Machines', names=useColumns)
        except Error as e:
            print(f'Error1: Processing {inputFile}, error {e}')
            continueProcessing = False

    if continueProcessing:
        try:        
            tidyDataFrame(df_machine_data)
            convertTimestampsToNewCols('ActiveDateString', 'ActiveTimeString', df_machine_data[activatedColumnName], df_machine_data)
            convertTimestampsToNewCols('ClearedDateString', 'ClearedTimeString', df_machine_data[clearedColumnName], df_machine_data)
        except Error as e:
            print(f"Error2: Problem with data frame? {e}")
            continueProcessing = False

    if continueProcessing:
        try:
            conn = sqlite3.connect(dbFile)
            df_machine_data.to_sql(name='machine_data', con=conn, if_exists='append')
        except Error as e:
            print(f"Error3: Processing database file {e}")
        finally:
            conn.close()

    if continueProcessing:
        updateProcessedList(reportFile, "that")


basePath = r'/media/ka/51195D827A36E8AA/Dev/Dev/FaultCodes'
parseFile = r'files_to_parse.txt'
processedListFileName = r'processed_files.txt'
fileToParse = os.path.join(basePath, parseFile)

try:
    f = open(fileToParse, 'r')
    processList = f.readlines()
except:
    print("Cannot find list of files to process")
finally:
    try:
        f.close()
    except:
        print('No file to close')


dbFile = 'MainDb.db'
dbaseFile = os.path.join(basePath, dbFile)
for item in processList:
    if '.xlsx' in item:
        # print(f"Opening file {item}")
        ProcessFileToSql(inputFile=item, dbFile=dbaseFile, reportFile=processedListFileName)
        # print("")
    else:
        print(f"Ignoring line {item}")





