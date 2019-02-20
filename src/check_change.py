#!/usr/bin/env python
# -*- coding: utf-8 -*-
from webspider import *
from filescan import *
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
workbook = xlrd.open_workbook("utilities_for_OWRS.xlsx")
urls = []
sheet = workbook.sheet_by_name("utilities_for_OWRS.csv")
for i in range(1, 11):
    line = sheet.row_values(i)
    utility_id, url = line[3], line[7]
    urls.append((utility_id, url))     
    
changes = []
for i in range(len(urls)):
    tests = check(urls[i][0], urls[i][1])
    if tests:
        heads, items = get_item(urls[i][0], urls[i][1])
        if not tests == items:
            print("changes" + " " + str(urls[i][0]))
            changes.append(urls[i])

if changes:
    for i in range(len(changes)):
        webspider(changes[i][0], changes[i][1])
