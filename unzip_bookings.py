__author__ = 'jpisano'

import os
import zipfile
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

# Main()
download_file = 'Daily_Bookings_Nexus_9K-91007.zip'
download_dir = 'c:/users/jpisano/downloads/'
working_dir = 'c:/users/jpisano/desktop/ACI to Production Database/Todays Data/'
working_file = 'Daily_Bookings_Nexus_9K.xlsm'
get_new_zip_file(download_dir, download_file, working_dir, working_file)