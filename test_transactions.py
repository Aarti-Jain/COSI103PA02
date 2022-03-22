import pytest
from transactions import Transactions

@pytest.mark.fixture
def testSummarize():
    trans = Transactions('tracker.db')
    categories = trans.summarize()
    assert categories[0] == ('investments',)
    assert categories[1] == ('purchases',)

