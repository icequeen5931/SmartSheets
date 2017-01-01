__author__ = 'jpisano'

import mysql.connector
import os
import openpyxl
from my_functions import table_exists,get_new_zip_file,csv_from_excel,stamp_it
from datetime import datetime

#
#
# Main()
#
#
cnx = mysql.connector.connect(user='root', password='Wdst12498', host='localhost', database='cust_ref_db')
mycursor = cnx.cursor()

download_file = 'Daily_Bookings_Nexus_9K-91007.zip'
download_dir = 'c:/users/jpisano/downloads/'
working_dir = 'c:/users/jpisano/desktop/ACI to Production Database - Beta/'
working_file = 'Daily_Bookings_Nexus_9K.xlsm'
todays_date = datetime.now()
as_of_date = todays_date.strftime('_as_of_%m_%d_%Y')

#Load coverage and PID tables as needed#

# Got Coverage ?
if table_exists(mycursor,'coverage') :
    sql = "DROP TABLE coverage"
    mycursor.execute(sql)

sql = ("CREATE TABLE coverage ("
       "`PSS` text,"
       "`TSA` text,"
       "`Sales Level 1` text,"
       "`Sales Level 2` text,"
       "`Sales Level 3` text,"
       "`Sales Level 4` text,"
       "`Sales Level 5` text,"
       "`Fiscal Year` text ) ")
mycursor.execute(sql)
cnx.commit()

sql = ("load data local infile '" + working_dir + "coverage.csv" + "' into table coverage "
        "fields terminated by ',' "
	    "enclosed by '\"' "
        "escaped by '' "
        "lines terminated by '\r\n' "
        "ignore 1 lines")
mycursor.execute(sql)
cnx.commit()
print("Updated Coverage Table !")

#Got PIDS ?
if table_exists(mycursor,'pids') :
    sql = "DROP TABLE pids"
    mycursor.execute(sql)

sql = ("CREATE TABLE `pids` ("
    "`Product Family` text,"
    "`Product ID` text,"
    "`Description` text)")
mycursor.execute(sql)
cnx.commit()

sql = ("load data local infile '" + working_dir + "pids.csv" + "' into table pids "
        "fields terminated by ',' "
	    "enclosed by '\"' "
        "escaped by '' "
        "lines terminated by '\r\n' "
        "ignore 1 lines")
mycursor.execute(sql)
cnx.commit()
print("Updated Product IDs Table !")

#Get todays file from download dir, copy to todays_data and rename it
if os.path.exists(download_dir + download_file):
    get_new_zip_file(download_dir + download_file, working_dir + 'todays_bookings_data')
    #Stamp it and save it
    stamp_it(download_dir+download_file,as_of_date)
else:
    print()
    print('Bookings Data not yet downloaded. Please download current copy !')

print("Processing NEW Bookings Data...")
csv_from_excel(working_dir+'todays_bookings_data/'+working_file,'Data')
#Stamp it and save it
stamp_it(working_dir + 'todays_bookings_data/' + working_file, as_of_date)

