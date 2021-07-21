import sqlite3

conn = sqlite3.connect("../outData/outputDatabase.db")
print("succeed to connect database")

c = conn.cursor()

sql = """ """
c.execute(sql)
