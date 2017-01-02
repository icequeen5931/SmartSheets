__author__ = 'jpisano'
from datetime import datetime

#database configuration settings

database = dict(
    DATABASE = "cust_ref_db",
    USER     = "root",
    PASSWORD = "Wdst12498",
    HOST     = "localhost"
)

#application predefined constants

app = dict(
    VERSION   = 1.0,
    GITHUB    = "{url}",
    DOWNLOAD_FILE = 'Daily_Bookings_Nexus_9K-91007.zip',
    DOWNLOAD_DIR = 'c:/users/jpisano/downloads/',
    WORKING_DIR = 'c:/users/jpisano/desktop/ACI to Production Database - Beta/',
    WORKING_FILE = 'Daily_Bookings_Nexus_9K.xlsm',
    WORKING_CSV_FILE = 'Daily_Bookings_Nexus_9K.csv',
    WORKING_DATA_DIR = 'todays_bookings_data/',
    AS_OF_DATE = datetime.now().strftime('_as_of_%m_%d_%Y')
)


#print(app["AS_OF_DATE"])