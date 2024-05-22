from preprocessing import preprocess, preprocess_comments
from pathways_code import Code

def count(s: str):
    return s.count("X"), s.count("Y"), s.count("#")

def _do_comment(to_test):
    return str(preprocess_comments(Code(to_test)))
    


def test_one_horiz_comment():
    totest = "ABC#DEF#GHI"
    res = _do_comment(totest)
    assert res == "ABC     GHI"