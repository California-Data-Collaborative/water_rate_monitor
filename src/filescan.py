#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import re
from lxml import html
from bs4 import BeautifulSoup
import os
import json
import os.path
import xlwt
import xlrd
from xlutils.copy import copy

# read information from stored excel files
def check(utility_id, url):
    tests = []
    #if os.path.isfile(url.split("www.")[1].split("/")[0] + ".xls"):
    try:
        workbook = xlrd.open_workbook(str(utility_id) + ".xls")
        sheet_names = workbook.sheet_names()
        for sheet_name in sheet_names:
            test = []
            sheet = workbook.sheet_by_name(sheet_name)
            for i in range(1, sheet.nrows):
                line = sheet.row_values(i)
                line = [x for x in line if x != '']
                if line == []:
                    continue
                test.append(line)      
            tests.append(test)
        return tests
    except:
        return            