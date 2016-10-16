__author__ = 'jpisano'
import requests
import json
import pprint

url = 'https://api.smartsheet.com/2.0/sheets'
#sheetuser = ''
#sheetpassword = ''

myheader = {'Authorization' : 'Bearer 519zl07z3k1uef6rfjxqqm5630'}

#payload = {
#  "index": "5",
#  "title": "my1stcol",
#  "type": "TEXT_NUMBER"
#}

#response = requests.post (url,data=json.dumps(payload),headers=myheaders,auth=(sheetuser,sheetpassword)).json()

response = requests.get (url, headers = myheader)
data = json.loads(response.text)

#pprint.pprint (response.text)
print ("-------------------------------------jim-------------------------------")
#print json.dumps(response.text)
mycnt = 0

for sheet in data["data"]:
    #print (sheet)
    #mycnt = mycnt +1
    #print (mycnt)
    #for v in sheet.values() :
    #for sheet in sheets.items():
    #for k in sheet.keys() :
        #if k in 'name':
        #if sheet.key["name"] in 'ACI to Production Dashboard 8-18-15':
        #print (v, end="")
            print ("SmartSheet: ",sheet['id'],sheet['name'])
               # print (k,end="")




