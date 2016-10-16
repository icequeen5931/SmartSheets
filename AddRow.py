__author__ = 'jpisano'

import requests
import json

sheetid = '4816554870237060'  # "test" Sheet ID
rowid = '4542989902079876'  # row number 4
colid = '4113607471458180'  # Customer Col ID
customer_col = '4113607471458180'  # Customer name

url = 'https://api.smartsheet.com/2.0/sheets/' + sheetid + '/rows'
myheader = {'Authorization': 'Bearer 519zl07z3k1uef6rfjxqqm5630', 'Content-Type': 'application/json'}

payload = {
    "toTop": True,
    "cells": [
        {
            "columnId": 4113607471458180,
            "value": "Jims Row"
        }
    ]
}

response = requests.post (url,headers=myheader,json=payload)
print (response.url)
print (response.content)
print (response.text)
data = json.loads(response.text)