#read or write data to excel (xls)
import xlrd
from xlutils.copy import copy
import os
#read excel
def readxls(filepath):
    wb = xlrd.open_workbook(filepath)
    return wb



def closexls(wb):
    wb.close()
