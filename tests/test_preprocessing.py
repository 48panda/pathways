from itertools import zip_longest
from preprocessing import preprocess, preprocess_comments
from pathways_code import Code

def _do_comment(to_test):
    return str(preprocess_comments(Code(to_test)))

def htov(s: str) -> str:
    return "\n".join(map("".join,zip_longest(*s.split("\n"),fillvalue=" ")))

def test_htov():
    assert htov("ab\ncd") == "ac\nbd"
    assert htov("ab\n\ncd") == "a c\nb d"
    assert htov("ab\ncd\nefg") == "ace\nbdf\n  g"

def test_one_horiz_comment():
    totest = "ABC#DEF#GHI"
    res = _do_comment(totest)
    assert res == "ABC     GHI"

def test_one_vert_comment():
    totest = htov("ABC#DEF#GHI")
    res = _do_comment(totest)
    assert res == htov("ABC     GHI")

def test_two_horiz_comment():
    totest = "ABC#DEF#GHI\nABC#DEF#GHI"
    res = _do_comment(totest)
    assert res == "ABC     GHI\nABC     GHI"

def test_two_vert_comment():
    totest = htov("ABC#DEF#GHI\nABC#DEF#GHI")
    res = _do_comment(totest)
    assert res == htov("ABC     GHI\nABC     GHI")