__author__ = 'jpisano'

import datetime
from my_functions import csv_from_excel
from os import sys


#path_to_import = 'c:/users/jpisano/desktop/ACI to Production Database/Todays Data/'
path_to_import = 'c:/users/jpisano/desktop/ACI to Production Database - Beta/Todays Data/'
file_to_import = 'Daily_Bookings_Nexus_9K 7-10-16.xlsx'

#file_to_get = path_to_import + file_to_import
csv_from_excel(path_to_import,file_to_import)
