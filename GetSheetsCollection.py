__author__ = 'jpisano'
import requests
import json
import csv
import pprint

url = 'https://api.smartsheet.com/2.0/sheets'

myheader = {'Authorization' : 'Bearer 519zl07z3k1uef6rfjxqqm5630', 'Content-Type':'application/json'}
#myheader = {'Authorization' : 'Bearer 519zl07z3k1uef6rfjxqqm5630', 'Content-Type':'text/plain','Accept': 'text/csv'}
#myheader = {'Authorization' : 'Bearer 519zl07z3k1uef6rfjxqqm5630', 'Accept':'text/csv'}

response = requests.get (url, headers=myheader)
print()
print('request   ',response.request.headers)
print()
print('headers   ',response.headers)
print()
print('text     ',response.text)
print()
print('content    ',response.content)
print()
print('status    ',response.status_code)
# csv.reader(response)
# print (response)
# print(type(response))
# jim = response.json()
# print(jim)

# data = json.loads(response.text)
#print(data)
# #sheets = data["data"]
# #print(type(sheets))
# for sheet in sheets:
    #if sheet["name"] in 'test':
    #print (sheet)
    # if sheet["name"].startswith('cust_ref_'):
    #     print ("SmartSheet: ",sheet['id'],sheet['name'])
    #     #sheet_id = sheets[('name')]

        #sheet_id = sheets

#print(type(sheet_id),sheet_id)

#url = 'https://api.smartsheet.com/2.0/sheets'
