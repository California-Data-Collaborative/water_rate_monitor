#!/usr/bin/env python
# -*- coding: utf-8 -*-
from webspider import *
from filescan import *

workbook = xlrd.open_workbook("utilities_for_OWRS.xlsx")
urls = []
sheet = workbook.sheet_by_name("utilities_for_OWRS.csv")
for i in range(1, 11):
    line = sheet.row_values(i)
    utility_id, url = line[3], line[7]
    urls.append((utility_id, url))     
    
for i in range(len(urls)):
    webspider(urls[i][0], urls[i][1])
