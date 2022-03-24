import pytest
from transactions import Transactions, to_trans_dict

#Test for part 10, summarize() - Aarti Jain
@pytest.mark.fixture
def testSummarize():
    trans = Transactions('tracker.db')
    categories = trans.summarize()
    assert categories[0] == ('investments',)
    assert categories[1] == ('purchases',)


# #Test for to_trans_dict - Aarthi Sivasankar
@pytest.mark.simple
def test_to_trans_dict():
    ''' teting the to_trans_dict function '''
    a = to_trans_dict((6,100,'testtranscategory', 'testtransdate', 'testtransdesc'))
    assert a['item_number']==6
    assert a['amount']==100
    assert a['category']=='testtranscategory'
    assert a['date']=='testtransdate'
    assert a['desc']=='testtransdesc'
    assert len(a.keys())==5

@pytest.fixture
def dbfile(tmpdir):
    ''' create a database file in a temporary file system '''
    return tmpdir.join('test_tracker.db')

@pytest.fixture
def empty_db(dbfile):
    ''' create an empty database '''
    db = Transactions(dbfile)
    yield db


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
        s = str(i)
        trans ={'amount':0+s, 'category':'category'+s, 'date': 'date'+s, 'desc':'description '+s,
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
    assert len(trans1) == len(trans0) + 1
#Test for Delete - Leora Kelsey
@pytest.mark.delete
def test_delete(med_db):
    ''' add a category to db, delete it, and see that the size changes'''
    # first we get the initial table
    cats0 = med_db.select_all()

    # then we add this category to the table and get the new list of rows
    cat0 = {'amount':700,
            'category':'see if it works',
            'date': '1/1/2022',
            'desc': 'Happy New Year Bonus',
            }
    rowid = med_db.add(cat0)
    cats1 = med_db.select_all()

    # now we delete the category and again get the new list of rows
    med_db.delete(rowid)
    cats2 = med_db.select_all()

    assert len(cats0)==len(cats2)
    assert len(cats2) == len(cats1)-1

@pytest.mark.sum_month
def test_sum_month(small_db):
    pass

@pytest.mark.sum_year
def test_sum_year(small_db):
    pass   
