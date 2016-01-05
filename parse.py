__author__ = 'Razin'

import re


def refine(pattern, data):
    if re.search(pattern, data, flags=re.IGNORECASE):
        return True
    else:
        return False


def parse(sheet, row, column):
    if sheet.cell(row, column).value:
        return sheet.cell(row, column).value
    else:
        return False


def status_check(data):
    if refine("COMPLETE", data):
        return True
    else:
        return False


