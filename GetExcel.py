__author__ = 'jpisano'

import requests

#ACI to Production Sheet
#sheetid = '4348263848535940'

#test sheet ID
sheetid= '4816554870237060'

url = 'https://api.smartsheet.com/2.0/sheets/' + sheetid
myheader = {'Authorization' : 'Bearer 519zl07z3k1uef6rfjxqqm5630','Accept':'application/vnd.ms-excel'}

response = requests.get (url, headers = myheader)
output = open('jim.xls','wb')
output.write (response.content)
