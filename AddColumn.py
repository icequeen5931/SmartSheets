__author__ = 'jpisano'

import requests
import json

sheetid = '4816554870237060'  # "test" Sheet ID
rowid = '4542989902079876'  # row number 4
customer_col = '4113607471458180'  # Customer name

url = 'https://api.smartsheet.com/2.0/sheets/' + sheetid + '/columns'
myheader = {'Authorization': 'Bearer 519zl07z3k1uef6rfjxqqm5630', 'Content-Type': 'application/json'}

response = requests.post (url,headers=myheader,json={"index": "5", "title": "my1stcol", "type": "TEXT_NUMBER"})
print (response.url)
print (response.content)
data = json.loads(response.text)
