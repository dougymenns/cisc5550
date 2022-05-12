import sqlite3

conn = sqlite3.connect('users.db')

c = conn.cursor()

c.execute('CREATE TABLE users (id INTEGER PRIMARY KEY,full_name text, email text, phone text, password text)')
c.execute('CREATE TABLE entries (what_to_do text, due_date text, status text)')
c.execute('select * from users')
print(c.fetchall())

conn.commit()

conn.close()