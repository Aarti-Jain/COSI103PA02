import sqlite3


nameOfFile = ""
def __init__(fileName):
    nameOfFile = fileName

#creating the table transactions
def create_table():
    con= sqlite3.connect(nameOfFile)
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS transactions
                (item_number INT AUTO_INCREMENT PRIMARY KEY,amount INT,category VARCHAR,date VARCHAR,description VARCHAR)''')

#Part 10: Summarize transactions by category
def summarize():
    con= sqlite3.connect(nameOfFile)
    cur = con.cursor()
    return cur.execute("SELECT * FROM transactions ORDER BY category")