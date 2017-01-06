__author__ = 'jpisano'

import os
from my_functions import get_new_zip_file,csv_from_excel,stamp_it
from settings import app,database
from prep_sql import prep_sql
from create_cust_data import create_cust_data
from export_cust_list import export_cust_list

def main():
    #
    # Main()
    #

    download_file = app['DOWNLOAD_FILE']
    download_dir = app['DOWNLOAD_DIR']
    working_dir = app['WORKING_DIR']
    working_file = app['WORKING_FILE']
    working_data_dir = app['WORKING_DATA_DIR']
    as_of_date = app['AS_OF_DATE']

    #Get todays bookings data from download dir, copy to todays_data and rename it
    if os.path.exists(download_dir + download_file):
        get_new_zip_file(download_dir + download_file, working_dir + working_data_dir)
        #Stamp it and save it
        stamp_it(download_dir+download_file,as_of_date)
    else:
        print()
        print('Bookings Data not yet downloaded. Please download current copy !')

    #Convert xls bookings file to CVS
    print("Processing NEW Bookings Data...")
    csv_from_excel(working_dir+working_data_dir+working_file,'Data')
    #Stamp it and save it
    stamp_it(working_dir + working_data_dir + working_file, as_of_date)
    #CSV file now prepped.

    #Import into new bookings data into MySQL
    prep_sql()
    #We now have a current master_bookings data table in MySQL

    #Summarize all bookings data (historical and current) into a master customer list
    create_cust_data()

    #Now we can export the new customer list as a CSV
    export_cust_list()


if __name__ == "__main__":
    main()


