import sqlite3
from sqlite3 import Error
import os

import matplotlib as mpl
import matplotlib.pyplot as plt

basePath = r'C:\Work\Fault_Code_Analysis'
dbFile = r'Maindb.db'
dbaseFile = os.path.join(basePath, dbFile)

startDate = '"2023-05-01"'
endDate = '"2023-09-16"'
exclusionList = "'D0228', 'P1434'"

line1 = f'SELECT "ERROR_CODE", "ERROR_DESCRIPTION", Count("ERROR_CODE") '
line2 = f'FROM machine_data WHERE "ActiveDateString" > {startDate} AND "ActiveDateString" < {endDate} '
line3 = f'AND "ERROR_CODE" NOT IN ({exclusionList}) '
line4 = f'GROUP BY "ERROR_CODE" '
line5 = f'ORDER BY Count("ERROR_CODE") DESC;'
query = line1+line2+line3+line4+line5

conn = sqlite3.connect(dbaseFile)
cursor = conn.cursor()
cursor.execute(query)
ErrorTotals = cursor.fetchall()
conn.close()

print(ErrorTotals)

count = 0
errorCode = []
frequency = []
print('[Occurrences], [Error Code], [Error Description]')
for item in ErrorTotals:
    if count < 20:
        errorCode.append(item[0])
        frequency.append(item[2])
        print(f"[{item[2]}] [{item[0]}] [{item[1]}]")
    else:
        break
    count += 1

fix, ax = plt.subplots()
# ax.bar(errorCode, frequency)
bars=plt.bar(errorCode, height=frequency)
plt.suptitle(f"Top 20 Error Codes from {startDate} to {endDate}")
plt.title(f'Excluding fault codes : {exclusionList}')
plt.xticks(rotation=90)
plt.xlabel("Top 20 Fault Codes")
plt.ylabel("Occurrences")
plt.grid('both')
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x(), yval + .005, yval)
plt.show()

