import sqlite3

def to_trans_dict(trans_tuple):
    ''' trans is a transaction tuple (item_number, amount, category, date, description)'''
    t = {'item_number':trans_tuple[0], 'amount':trans_tuple[1], 'category':trans_tuple[2], 'date':trans_tuple[3], 'desc':trans_tuple[4]}
    return t

def to_trans_dict_list(trans_tuples):
    ''' convert a list of category tuples into a list of dictionaries'''
    return [to_trans_dict(t) for t in trans_tuples]

class Transactions():

    def __init__(self,fileName):
        con= sqlite3.connect(fileName)
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS transactions
                (item_number INT AUTO_INCREMENT PRIMARY KEY,amount INT,category VARCHAR,date VARCHAR,desc VARCHAR)''')
        con.commit()
        con.close()
        self.fileName = fileName

   #Part 4: To select transactions to be shown
    def select_all(self):
        ''' return all of the transactions as a list of dicts.'''
        con= sqlite3.connect(self.fileName)
        cur = con.cursor()
        cur.execute("SELECT item_number,* from transactions")
        tuples = cur.fetchall()
        con.commit()
        con.close()
        return to_trans_dict_list(tuples)

    #Part 5: To add transactions 
    def add(self,item): 
        ''' add a transaction to the transactions table.
            this returns the item_number of the inserted element
        '''
        con= sqlite3.connect(self.fileName)
        cur = con.cursor()
        cur.execute("INSERT INTO transactions VALUES(?,?)",(item['amount'],item['category'],item['date'], item['desc']))
        con.commit()
        cur.execute("SELECT last_insert_item_number()")
        last_item_number = cur.fetchone()
        con.commit()
        con.close()
        return last_item_number[0]

   #Part 10: Summarize transactions by category
    def summarize(self):
       con= sqlite3.connect(self.fileName)
       cur = con.cursor()
       return cur.execute("SELECT * FROM transactions ORDER BY category")









 #nameOfFile = ""
#def __init__(fileName):
#    nameOfFile = fileName

#creating the table transactions
#def create_table():
#    con= sqlite3.connect(nameOfFile)
#    cur = con.cursor()