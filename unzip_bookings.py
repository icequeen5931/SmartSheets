__author__ = 'jpisano'

import os
import zipfile
import mysql.connector
from datetime import datetime

def get_new_zip_file(download_dir, download_file, working_dir, working_file):
    #Build a timestamp
    timestamp = str(datetime.now())
    timestamp = timestamp.replace(':', '_')
    timestamp = timestamp.replace('-', '_')
    timestamp = timestamp.replace('.', '_')

    # Is there a bookings file downloaded ?
    if os.path.exists(download_dir + download_file):

        # Does the working file exist ? if so let's rename it
        if os.path.exists(working_dir):
            try:
                #Rename and timestamp the existing  file
                os.rename(working_dir + working_file, working_dir + '\ ' + timestamp + '_' + working_file)
                print()
                print("Previous bookings data renamed to: "+ timestamp + '_' + working_file)
            except FileNotFoundError as err:
                print()
                print("Just FYI - No existing file to rename")

            #Unzip the file into the specified path
            zip_ref = zipfile.ZipFile(download_dir + download_file)
            zip_ref.extractall(working_dir)

            # close out the zip file
            zip_ref.close()

            #timestamp and rename the downloaded bookings file
            os.rename(download_dir + download_file, download_dir + '\ ' + timestamp + '_' + download_file)
            print()
            print("New Bookings Data File Ready !")
    else:
        print()
        print('Bookings Data not yet downloaded. Please download current copy !')
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
#working_dir = 'c:/users/jpisano/desktop/ACI to Production Database/Todays Data/'
working_file = 'Daily_Bookings_Nexus_9K.xlsm'
todays_date = datetime.now()
as_of_date = todays_date.strftime('_as_of_%m_%d_%Y')

print (todays_date.strftime('%Y/%m/%d'), as_of_date)

#Drop all tables that will be rebuilt

sql= "SELECT * FROM information_schema.tables WHERE table_name = 'coverage'"
mycursor.execute(sql)
if mycursor.fetchone() != None :
    #Load Coverage and PID tables
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
print (sql)
mycursor.execute(sql)
cnx.commit()












#Get todays file from download, copy to todays_data and rename it
#get_new_zip_file(download_dir, download_file, working_dir, working_file)