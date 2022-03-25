'''TO DO: This is our tests'''
import pytest
from transactions import Transactions, to_trans_dict

#Test for part 10, summarize() - Aarti Jain
@pytest.mark.fixture
def test_summarize():
    '''Hark! A test!'''
    trans = Transactions('tracker.db')
    categories = trans.summarize()
    assert categories[0] == ('purchases',)
   

# #Test for to_trans_dict - Aarthi Sivasankar
@pytest.mark.simple
def test_to_trans_dict():
    ''' teting the to_trans_dict function '''
    dic = to_trans_dict((6,100,'testtranscategory', 'testtransdate', 'testtransdesc'))
    assert dic['item_number']==6
    assert dic['amount']==100
    assert dic['category']=='testtranscategory'
    assert dic['date']=='testtransdate'
    assert dic['desc']=='testtransdesc'
    assert len(dic.keys())==5


@pytest.fixture
def dbfile(tmpdir):
    ''' create a database file in a temporary file system '''
    return tmpdir.join('test_tracker.db')


@pytest.fixture
def empty_db(dbfile):
    ''' create an empty database '''
    dbs = Transactions(dbfile)
    yield dbs


@pytest.fixture
def small_db(empty_db):
    ''' create a small database, and tear it down later'''
    trans1 = {'amount':100,'category':'food','date':'03/18/2022','desc':'takeout'}
    trans2 = {'amount':200,'category':'phone','date':'03/19/2022','desc':'iphone'}
    trans3 = {'amount':300,'category':'clothes','date':'03/20/2022','desc':'dress'}
    id1=empty_db.add(trans1)
    id2=empty_db.add(trans2)
    id3=empty_db.add(trans3)
    yield empty_db
    empty_db.delete(id3)
    empty_db.delete(id2)
    empty_db.delete(id1)


@pytest.fixture
def med_db(small_db):
    ''' create a database with 10 more elements than small_db'''
    itemnumbers=[]
    # add 10 transactions
    for i in range(10):
        sums = str(i)
        trans ={'amount':0+int(sums),
        'category':'category'+sums, 'date': 'date'+sums, 'desc':'description '+sums,
                }
        item_number = small_db.add(trans)
        itemnumbers.append(item_number)

    yield small_db

    # remove those 10 categories
    for j in range(10):
        small_db.delete(itemnumbers[j])


#Test for add - Aarthi Sivasankar
@pytest.mark.add
def test_add(med_db):
    ''' add a transaction to db, the select it, then delete it'''

    trans0 = {'amount':100,'category':'testcategory','date':'testdate','desc':'testdesc'}
    transo = med_db.select_all()
    item_number = med_db.add(trans0)
    trans1 = med_db.select_all()
    assert len(trans1) == len(transo) + 1


#Test for Delete - Leora Kelsey
@pytest.mark.delete
def test_delete(empty_db):
    '''A simple test to see if delete deletes as expected'''
    # first we test if the db is empty as expected
    assert len(empty_db.select_all()) == 0
    cats0 = empty_db.select_all()
    #this was a test bc it wasn't working before
    assert len(cats0) == 0
    #These are what are getting to the db
    cat0 = {'amount':700,
            'category':'see if it works',
            'date': '01/01/2022',
            'desc': 'Happy New Year Bonus',
            }
    cat1 = {'amount':600,
            'category':'take2',
            'date': '01/02/2022',
            'desc': 'new bonus',
            }
    #adding the first
    empty_db.add(cat0)
    cats1 = empty_db.select_all()
    #asserting correct length
    assert len(cats1) == 1
    empty_db.add(cat1)
    cats2 = empty_db.select_all()
    #again, asserting correct length
    assert len(cats2) == 2
    #starting deletion
    empty_db.delete(2)
    cats3 = empty_db.select_all()
    #now that we've deleted, time to test the size
    assert len(cats3) == 1
    empty_db.delete(1)
    cats4 = empty_db.select_all()
    #asserting now that we've manually deleted both of them,
    # that the size is correct
    assert len(cats4) == 0


#Test for Delete - Leora Kelsey
@pytest.mark.delete
def test_delete2(med_db):
    ''' add a category to db, delete it, and see that the size changes'''
   #I created an extra test because I wanted a more complicated version
    cats0 = med_db.select_all()
    cat0 = {'amount':700,
            'category':'see if it works',
            'date': '01/01/2022',
            'desc': 'Happy New Year Bonus',
            }
    cat1 = {'amount':600,
            'category':'take2',
            'date': '01/02/2022',
            'desc': 'new bonus',
            }
    med_db.add(cat0)
    cats1 = med_db.select_all()
    #asserting size is right
    assert len(cats1) == len(cats0)+1
    med_db.add(cat1)
    cats2 = med_db.select_all()
    #asserting size is right again
    assert len(cats2) == len(cats1) +1
    assert len(cats2) == len(cats0) +2
    med_db.delete(2)
    cats3 = med_db.select_all()
    #cats3 is after 2 additions and 1 deletion, cats1 is 1 additions
    #they should be the same size
    assert len(cats3) == len(cats1)
    med_db.delete(1)
    cats4 = med_db.select_all()
    #checking that its the same size as the start, cats0
    assert len(cats4) == len(cats0)


@pytest.mark.sum_date
def test_sum_date(empty_db):
    '''tests whether the items are printed out in the proper order'''
    #1- chronology
    cat0 = {'amount':700,
            'category':'see if it works',
            'date': '06/01/2002',
            'desc': 'Happy New Year Bonus',
            }
    #3 chronology
    cat1 = {'amount':700,
            'category':'see if it works',
            'date': '11/03/2000',
            'desc': 'Happy New Year Bonus',
            }
    #2 chronology
    cat2 = {'amount':700,
            'category':'see if it works',
            'date': '01/02/2000',
            'desc': 'Happy New Year Bonus',
            }
    empty_db.add(cat0)
    empty_db.add(cat1)
    empty_db.add(cat2)
    #the default order (cat0, cat1, cat2)
    items2 = empty_db.select_all()
    num = 0
    for item in items2:
        num += 1
        if num == 1:
            assert item[3] == '06/01/2002'
        if num == 2:
            assert item[3] == '11/03/2000'
        if num == 3:
            assert item[3] == '01/02/2000'
    #orders them via date (cat2, cat1, cat0)
    items1 = empty_db.sum_date()
    num = 0
    for item in items1:
        num += 1
        if num == 1:
            assert item[3] == '01/02/2000'
        if num == 2:
            assert item[3] == '11/03/2000'
        if num == 3:
            assert item[3] == '06/01/2002'


# Part 8 - Elizabeth Diener
@pytest.mark.sum_month
def test_sum_month(empty_db):
    """_summary_
    This pytest will test whether the function sum_month returns items sorted by ONLY the month aspect of the date.
    """
    # Create three categories
    cat0 = {'amount':700, 'category':'testing', 'date': '06/01/2002', 'desc': 'Whatever',}
    cat1 = {'amount':700, 'category':'testing', 'date': '11/03/2000', 'desc': 'Whatever',}
    cat2 = {'amount':700, 'category':'testing', 'date': '01/02/2000', 'desc': 'Whatever',}
    
    # Add the three categories in the order cat0, cat1, cat2
    empty_db.add(cat0)
    empty_db.add(cat1)
    empty_db.add(cat2)
    
    # Testing the order by month (cat2, cat0, cat1)
    items_order_month = empty_db.sum_month()
    num = 0
    for item in items_order_month:
        num += 1
        if num == 1:
            assert item[3] == '01/02/2000'
        if num == 2:
            assert item[3] == '06/01/2002'
        if num == 3:
            assert item[3] == '11/03/2000'
    

# Part 9 - Elizabeth Diener
@pytest.mark.sum_year
def test_sum_year(empty_db):
    """_summary_
    This pytest will test whether the function sum_year returns items sorted by ONLY the year aspect of the date.
    """
    # Create three categories
    cat0 = {'amount':700, 'category':'testing', 'date': '06/01/2002', 'desc': 'Whatever',}
    cat1 = {'amount':700, 'category':'testing', 'date': '11/03/2000', 'desc': 'Whatever',}
    cat2 = {'amount':700, 'category':'testing', 'date': '01/02/2000', 'desc': 'Whatever',}
    
    # Add the three categories in the order cat0, cat1, cat2
    empty_db.add(cat0)
    empty_db.add(cat1)
    empty_db.add(cat2)
    
    # Testing the order by month (cat1, cat2, cat0)
    items_order_year = empty_db.sum_year()
    num = 0
    for item in items_order_year:
        num += 1
        if num == 1:
            assert item[3] == '11/03/2000'
        if num == 2:
            assert item[3] == '01/02/2000'
        if num == 3:
            assert item[3] == '06/01/2002'
