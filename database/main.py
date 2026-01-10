import sqlite3
con = sqlite3.connect("handmade.db")
cur = con.cursor()

cur.execute("CREATE TABLE sites(url, text)")
cur.execute("CREATE TABLE webIndex(keyword, site, score)")

res = cur.execute("SELECT * FROM sites")

print(res.fetchone())

