__author__ = 'jpisano'


import mysql.connector
import os
from my_functions import table_exists,get_new_zip_file,csv_from_excel,stamp_it
from datetime import datetime
from settings import app,database

#
#
# Main()
#
#
cnx = mysql.connector.connect(user=database['USER'], password=database['PASSWORD'], host=database['HOST'], database=database['DATABASE'])
mycursor = cnx.cursor()

download_file = app['DOWNLOAD_FILE']
download_dir = app['DOWNLOAD_DIR']
working_dir = app['WORKING_DIR']
working_file = app['WORKING_FILE']
working_data_dir = app['WORKING_DATA_DIR']
as_of_date = app['AS_OF_DATE']

#todays_date = datetime.now()
#as_of_date = todays_date.strftime('_as_of_%m_%d_%Y')

#Prep SQL


#Get todays bookings data from download dir, copy to todays_data and rename it
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

#CSV file now prepped.
#Import into MySQL

