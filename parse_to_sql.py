import pandas as pd
import sqlite3
from sqlite3 import Error
import os

def convertTimestampsToNewCols(dateColName, timeColname, column, dataFrame):
    DateList = []
    TimeList = []

    print(column)

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
    removeColumns = ['Name', 'Machine Profile', 'Severity Description', 'DTC Code', 'Source Address (Decimal)',
                     'Script action(s)']
    for name in removeColumns:
        if name in dataFrame.columns:
            del dataFrame[name]


basePath = r'/media/ka/5ABECB1ABECAED97/Users/nonAdmin/Documents/PySqllite/'
inFile = r'COPY_Machine DTC History Results Sept and Oct OUT.xlsx'
dbFile = r'example.db'
inputFile = os.path.join(basePath, inFile)
dbaseFile = os.path.join(basePath, dbFile)

print(inputFile)
print(dbaseFile)

useColumns = ['VIN','Name','Machine Profile','MachineHours','Severity','Severity Description','DTC Code','SPN','FMI','Source Address (Decimal)','Source Address (Hexadecimal)','Activated Time','Cleared Time','Error Code','Error Code Description','Script action(s)']

xls = pd.ExcelFile(inputFile)
df_machine_data = pd.read_excel(xls, 'Machine DTC History Results Sep', names=useColumns)

tidyDataFrame(df_machine_data)

convertTimestampsToNewCols('ActiveDateString', 'ActiveTimeString', df_machine_data['Activated Time'], df_machine_data)
convertTimestampsToNewCols('ClearedDateString', 'ClearedTimeString', df_machine_data['Cleared Time'], df_machine_data)

conn = sqlite3.connect(dbaseFile)
df_machine_data.to_sql(name='machine_data', con=conn, if_exists='replace')
conn.close()

