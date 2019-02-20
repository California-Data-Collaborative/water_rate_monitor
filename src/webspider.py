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
from pathlib import Path
from xlutils.copy import copy

    
def excel_write(items, index, ws):
    for item in items:
        for i in range(0, len(item)):
            ws.write(index, i, item[i])
        index += 1

def get_item(utility_id, url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    tableTags = soup.find_all('table')
    if not tableTags:
        print("no_table" + " " + str(utility_id))
    heads = []
    items = []
    for table_index in range(len(tableTags)):
        tableTag = tableTags[table_index]
        # get head
        try:
            trHead = tableTag.thead.find_all('th')
            head = []
            for tag in trHead:
                head.append(tag.getText().strip())
        except:
            head = []
        # get item
        try:
            trTags = tableTag.tbody.find_all('tr')
            item = []
            for tag in trTags:
                line = []
                tags = tag.find_all('td')
                for i in range(len(tags)):
                    line.append(tags[i].getText().strip())
                line = [x for x in line if x != '']

                if line == []:
                    continue
                item.append(line)
        except:
            item = []
        heads.append(head)
        items.append(item)
    return heads, items


def webspider(utility_id, url):
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'lxml')
        tableTags = soup.find_all('table')
        heads, items = get_item(utility_id, url)
        
        # check if items form table is all empty
        try:
            if items:
                for i in range(len(items)):
                    if items[i] != []:
                         break
                if i == len(items) - 1:
                    print("no_table" + " " + str(utility_id))
                    tableTags = [] 
        except:
            pass
        
        # start crawl the information and save to excel (each table to one sheet)  
        index = 1
        for table_index in range(len(tableTags)):
            tableTag = tableTags[table_index]
            if table_index == 0:
                #newTable = url.split("www.")[1].split("/")[0] + ".xls"
                newTable = str(utility_id) + ".xls"
                wb = xlwt.Workbook(encoding='utf-8')
                ws = wb.add_sheet('sheet' + str(table_index))
            else:
                w = xlrd.open_workbook(str(utility_id) + ".xls")
                wb = copy(w)
                ws = wb.add_sheet('sheet' + str(table_index))

            headData = heads[table_index]
            for colnum in range(len(headData)):
                ws.write(0, colnum, headData[colnum], xlwt.easyxf('font: bold on'))
            excel_write(items[table_index], index, ws)
            wb.save(newTable)     
    except:
        print("no_webpage" + " " + str(utility_id))       
    return
