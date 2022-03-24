from tabnanny import check
from communication_grid import Grid
from evaluation_cost import *
import re

def check_symbol(word):
    res = (re.search("^/.+",word) or re.search(".+/$",word) or re.search(".+-$",word) or re.search("^-.+",word))
    if res:
        return True

    else:
        return False

word = "dedede"
check_symbol(word)