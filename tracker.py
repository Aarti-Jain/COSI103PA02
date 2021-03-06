#! /opt/miniconda3/bin/python3
'''
tracker is an app that maintains a list of personal
financial transactions.

It uses Object Relational Mappings (ORM)
to abstract out the database operations from the
UI/UX code.

The ORM, Category, will map SQL rows with the schema
  (rowid, category, description)
to Python Dictionaries as follows:

(5,'rent','monthly rent payments') <-->

{rowid:5,
 category:'rent',
 description:'monthly rent payments'
 }

Likewise, the ORM, Transaction will mirror the database with
columns:
amount, category, date (yyyymmdd), description

In place of SQL queries, we will have method calls.

This app will store the data in a SQLite database ~/tracker.db

Note the actual implementation of the ORM is hidden and so it
could be replaced with PostgreSQL or Pandas or straight python lists

'''
import sys
from transactions import Transactions
from category import Category


transact = Transactions('tracker.db')
category = Category('tracker.db')


# here is the menu for the tracker app

MENU = '''
0. quit
1. show categories
2. add category
3. modify category
4. show transactions
5. add transaction
6. delete transaction
7. summarize transactions by date
8. summarize transactions by month
9. summarize transactions by year
10. summarize transactions by category
11. print this menu
'''

def process_choice(choice):
    '''TO DO: write up docstring'''
    if choice=='0':
        return
    elif choice=='1':
        cats = category.select_all()
        print_categories(cats)
    elif choice=='2':
        name = input("category name: ")
        desc = input("category description: ")
        cat = {'name':name, 'desc':desc}
        category.add(cat)

    elif choice=='3':
        print("modifying category")
        rowid = int(input("rowid: "))
        name = input("new category name: ")
        desc = input("new category description: ")
        cat = {'name':name, 'desc':desc}
        category.update(rowid,cat)

    #part 4: show transactions
    elif choice=='4':
        trans = transact.select_all()
        print_transactions(trans)

    #part 5: add transaction
    elif choice=='5':
        amt = input("transaction amount: ")
        trans_cat = input("transaction category: ")
        date =  input("transaction date: ")
        trans_desc =  input("transaction description: ")
        trans = {'amount':amt, 'category':trans_cat, 'date':date, 'desc':trans_desc}
        transact.add(trans)

    #part 6: delete transaction - Leora Kelsey
    elif choice =='6':
        rowid = input("rowid: ")
        transact.delete(rowid)
    #part 7: summarize transactions by date - Leora Kelsey
    elif choice == '7':
        print_transactions(transact.sum_date())

    #part 8: summarize transactions by month - Elizabeth Diener
    elif choice == '8':
        transbymonth = transact.sum_month()
        print_transactions(transbymonth)

    #part 9: summarize transactions by year - Elizabeth Diener
    elif choice == '9':
        transbyyear = transact.sum_year()
        print_transactions(transbyyear)

    #part 10: summarize transactions by category - Aarti Jain
    elif choice == '10':
        categories = transact.summarize()
        for cat in categories:
            print(cat)

    #part 11: print menu - Aarti Jain
    elif choice == '11':
        print(MENU)

    else:
        print("choice",choice,"not yet implemented")

    choice = input("> ")
    return choice


def toplevel():
    ''' handle the user's choice '''

    ''' read the command args and process them'''
    print(MENU)
    choice = input("> ")
    while choice !='0' :
        choice = process_choice(choice)
    print('bye')

#
# here are some helper functions
#

def print_transactions(items):
    ''' print the transactions '''
    for item in items:
        print(item)

def print_category(cat):
    '''TO DO: write doc string'''
    print("%-3d %-10s %-30s"%(cat['rowid'],cat['name'],cat['desc']))

def print_categories(cats):
    '''TO DO: write doc string'''
    print("%-3s %-10s %-30s"%("id","name","description"))
    print('-'*45)
    for cat in cats:
        print_category(cat)


# here is the main call!

toplevel()
