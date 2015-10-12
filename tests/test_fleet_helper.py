

from datacleaning.fleet_helper import *
from pandas import DataFrame

def test_tag_selector():
    df = DataFrame(columns=['a1','a2','b1','b2'])
    t = tag_selector(df)
    assert (t.sub('1', ignorecase=False) == ['a1','b1'])
    assert (t.sub(['1', 'a'], ignorecase=False) == ['a1'])