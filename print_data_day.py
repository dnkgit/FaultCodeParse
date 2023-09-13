import sqlite3
from sqlite3 import Error
import os

import matplotlib as mpl
import matplotlib.pyplot as plt

basePath = r'/media/ka/5ABECB1ABECAED97/Users/nonAdmin/Documents/PySqllite/'
dbFile = r'example.db'
dbaseFile = os.path.join(basePath, dbFile)

conn = sqlite3.connect(dbaseFile)
cursor = conn.cursor()
cursor.execute('SELECT "Error Code", Count(*) FROM machine_data GROUP BY "Error Code" ORDER BY Count(*) DESC')
ErrorTotals = cursor.fetchall()
conn.close()

print(ErrorTotals)

count = 0
errorCode = []
frequency = []
for item in ErrorTotals:
    if count < 20:
        errorCode.append(item[0])
        frequency.append(item[1])
    else:
        break
    count += 1

fix, ax = plt.subplots()
# ax.bar(errorCode, frequency)
bars=plt.bar(errorCode, height=frequency)
plt.xticks(rotation=90)
plt.xlabel("Top 20 Fault Codes")
plt.ylabel("Occurrences")
plt.grid('both')
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x(), yval + .005, yval)
plt.show()