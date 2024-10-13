import sqlite3

con = sqlite3.connect("database.db")
cursor = con.cursor()

emails = [
    "khoi@example.com",
    "musubi-io@localhost",
    "khoi@demomailtrap.com",
    "tonytong011235813@gmail.com",
    "minhkhoitran@cpp.edu",
    "matttrv.kwong@gmail.com",
    "briha155@gmail.com"
]

for i, e in enumerate(emails):
    cursor.execute(f"INSERT INTO userEmail (id, email) VALUES ('{i}', '{e}')")

con.commit()
con.close()