''''Aarti, Aarthi, Elizabeth and Leora present our code'''
import sqlite3

def to_trans_dict(tran):
    ''' tran is a transaction tuple
    (item_number, amount, category, date, description)'''
    tdict={'item_number':tran[0],'amount':tran[1],'category':tran[2],'date':tran[3],'desc':tran[4]}
    return tdict
    #Can we change item_number into something shorter,
    # amount to amt, category to ctgry?
def to_trans_dict_list(trans_tuples):
    ''' convert a list of category tuples into a list of dictionaries'''
    return [to_trans_dict(t) for t in trans_tuples]

class Transactions():
    '''TO DO: put in a summary of what this does'''
    def __init__(self,file_name):
        con= sqlite3.connect(file_name)
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS transactions
                (item_number INT AUTO_INCREMENT PRIMARY KEY,
                amount INT,
                category VARCHAR,
                date VARCHAR,
                desc VARCHAR)''')
        con.commit()
        con.close()
        self.file_name = file_name

   #Part 4: To select transactions to be shown - Aarthi Sivasankar
    def select_all(self):
        ''' return all of the transactions as a list of dicts.'''
        con = sqlite3.connect(self.file_name)
        cur = con.cursor()
        cur.execute("SELECT item_number,* from transactions")
        tuples = cur.fetchall()
        con.commit()
        con.close()
        return tuples #to_trans_dict_list(tuples)
    #Part 5: To add transactions - Aarthi Sivasankar
    def add(self,itm):
        ''' add a transaction to the transactions table.
            this returns the item_number of the inserted element
        '''
        global itm_nm #This isn't fully declared and should be named with capitals
        itm_nm = 1
        con= sqlite3.connect(self.file_name)
        cur = con.cursor()
        cur.execute("INSERT INTO transactions VALUES(?,?,?,?,?)"
        ,(itm_nm,itm['amount'],itm['category'],itm['date'], itm['desc'])) #Does the code still work?
        con.commit()
        cur.execute("SELECT last_insert_item_number()")
        last_item_number = cur.fetchone()
        con.commit()
        con.close()
        itm_nm+=1
        return last_item_number[0]

    #Part 6: To delete transactions - Leora Kelsey
    def delete(self, rowid,):
        '''Deletes a transaction from the transaction table'''
        con = sqlite3.connect(self.file_name)
        cur = con.cursor()
        cur.execute("DELETE FROM transactions WHERE rowid=(?)", (rowid,))
        con.commit()
        con.close()

    #Part 7: Summarize transactions by date - Leora Kelsey
    def sum_date(self):
        '''TO DO: add docstring summary of this'''
        con = sqlite3.connect(self.file_name)
        cur = con.cursor()
        item = cur.execute("SELECT * FROM transactions ORDER BY date")
        return item
    #Part 8: Summarize transactions by month - Elizabeth Diener
    def sum_month(self):
        """_summary_
        This method returns a list of all transaction data in the file
        associated with the instance of this class, ordered by month.
        :return: All transactions ordered by month.
        :rtype: list[tuple]
        """
        con = sqlite3.connect(self.file_name)
        cur = con.cursor()
        return cur.execute("SELECT * FROM transactions ORDER BY strftime('%m', 'date') DESC")

    #Part 9: Summarize transactions by year - Elizabeth Diener
    def sum_year(self):
        """_summary_
        This method returns a list of all transaction data
        in the file associated with the instance of this class, ordered by year.
        :return: All transactions ordered by year.
        :rtype: list[tuple]
        """
        con = sqlite3.connect(self.file_name)
        cur = con.cursor()
        return cur.execute("SELECT * FROM transactions ORDER BY strftime('%Y', 'date') DESC")

   #Part 10: Summarize transactions by category - Aarti Jain
    def summarize(self):
        '''TO DO: add docstring summary of this'''
        con= sqlite3.connect(self.file_name)
        cur = con.cursor()
        cur.execute("SELECT category FROM transactions ORDER BY category")
        rows = cur.fetchall()
        results = []
        for row in rows:
            results.append(row)
        return results

    #Part 11 is located in tracker.py - Aarti Jain
