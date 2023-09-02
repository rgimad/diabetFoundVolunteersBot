import sqlite3

conn = sqlite3.connect('database.db') 
c = conn.cursor()

# c.execute('DROP TABLE IF EXISTS skills')
c.execute('DROP TABLE IF EXISTS users')

c.execute('''CREATE TABLE users (
            _id INTEGER PRIMARY KEY,
            fio TEXT,
            age INTEGER,
            city TEXT,
            diabet TEXT
        )''')

# c.execute('''CREATE TABLE skills (
#             _id        INTEGER PRIMARY KEY ,
            
#         )''')

conn.commit()
conn.close()


