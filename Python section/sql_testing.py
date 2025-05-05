import sqlite3

db = sqlite3.connect('first_db.db')

c = db.cursor()

# c.execute("""CREATE TABLE articles(
#           title text,
#           full_text text, 
#           views integer,
#           author text 
#           )
# """)

# c.execute("INSERT INTO articles VALUES ('Facebook is cool!', 'Facebook is reaaly cool!', 40, 'Moderator')")

c.execute("SELECT rowid, title FROM articles ")
items = c.fetchall()
for i in items: 
    print(i)
db.commit()
db.close()