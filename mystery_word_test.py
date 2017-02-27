from mystery_word import get_word_list
from mystery_word import clean_sentence
from mystery_word import is_repeat
from mystery_word import is_win


def test_get_word_list():
    assert get_word_list("easy", file='simple.txt') ==["quick", "brown",
                                                       "jumped", "over", "lazy",
                                                       "spot"]
    assert get_word_list("medium", file='simple.txt') == ["jumped", "bananas",
                                                          "function"]
    assert get_word_list("hard", file='simple.txt') == ["indivisible",
                                                        "function"]


def test_clean_sentence():
    assert clean_sentence("easy") == "easy"
    assert clean_sentence("a space") == "aspace"
    assert clean_sentence("Capitalized") == "capitalized"
    assert clean_sentence("$p3c*al~") == "pcal"
    assert clean_sentence("@LL 0p7*ons") == "llpons"


def test_is_repeat():
    assert is_repeat('a', ['a'], ['b'], 8) == True
    assert is_repeat('b', ['a'], ['b'], 8) == True
    assert is_repeat('c', ['a'], ['b'], 8) == False


def test_is_win():
    assert is_win("cat", ['c', 'a', 't']) == True
    assert is_win("dog", ['d', 'g']) == False
    assert is_win("poop", ['p', 'o']) == True
    assert is_win("bob", ['b']) == False


 test_get_word_list()
 test_clean_sentence()
 test_is_repeat()
 test_is_win()
