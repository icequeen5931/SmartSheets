__author__ = 'jpisano'

import mysql.connector

cnx = mysql.connector.connect(user='root', password='Wdst12498', host='localhost', database='cust_ref_db')
mycursor = cnx.cursor()

#
sql = "DROP TABLE master_bookings_data"
mycursor.execute(sql)
print("Deleted OLD Master Bookings Data...")
cnx.commit()

#
sql = "DROP TABLE todays_bookings_data"
mycursor.execute(sql)
print("Deleted Daily Bookings Data...")
cnx.commit()

# print("Processing NEW Bookings Data...")
# path_to_import = 'c:/users/jpisano/desktop/ACI to Production Database - Beta/Todays Data/'
# file_to_import = 'FY17_Daily_Bookings_Nexus_9K_as of_12_7_16.xlsx'
# csv_from_excel(path_to_import,file_to_import)

sql = ('CREATE TABLE master_bookings_data '
    '(`Fiscal Year` TEXT,'
    '`Fiscal Quarter ID` TEXT,'
    '`Fiscal Period ID` TEXT,'
    '`Fiscal Week ID` TEXT,'
    '`Date Booked` DATE,'
    '`Sales Level 1` TEXT,'
    '`Sales Level 2` TEXT,'
    '`Sales Level 3` TEXT,'
    '`Sales Level 4` TEXT,'
    '`Sales Level 5` TEXT,'
    '`Sales Level 6` TEXT,'
    '`Sales Agent Name` TEXT,'
    '`Internal Business Entity Name` TEXT,'
    '`Internal Sub Business Entity Name` TEXT,'
    '`Product Family` TEXT,'
    '`Product ID` TEXT,'
    '`End Customer Global Ultimate Name` TEXT,'
    '`End Customer Global Ultimate Company Target ID` TEXT,'
    '`Ship to ERP Customer Name` TEXT,'
    '`Sales Order Number Detail` TEXT,'
    '`ERP Deal ID` TEXT,'
    '`Corporate Bookings Flag` TEXT,'
    '`Partner Name` TEXT,'
    '`SCMS` TEXT,'
    '`Product Bookings Net` TEXT,'
    '`Service Bookings Net` TEXT,'
    '`Bookings Adjustments Description` TEXT ,'
    '`Hash Value` VARCHAR (32)) ')

mycursor.execute(sql)
cnx.commit()

sql= "CREATE TABLE todays_bookings_data LIKE master_bookings_data;"
mycursor.execute(sql)
print("Created NEW Master Bookings Data...")
cnx.commit()

print("Importing NEW Bookings Data...")
sql = ("load data local infile 'C:/Users/jpisano/Desktop/ACI to Production Database - Beta/Todays Data/FY17_Daily_Bookings_Nexus_9K_as of_12_7_16.csv' into table todays_bookings_data "
        "fields terminated by ',' "
	    "enclosed by '\"' "
        "escaped by '' "
        "lines terminated by '\r\n' ")
mycursor.execute(sql)
cnx.commit()

sql = "INSERT INTO master_bookings_data SELECT archive_bookings_data_fy15.* FROM archive_bookings_data_fy15"
mycursor.execute(sql)
print("Gathered FY15 Bookings Data...")
cnx.commit()

sql = "INSERT INTO master_bookings_data SELECT archive_bookings_data_fy16.* FROM archive_bookings_data_fy16"
mycursor.execute(sql)
print("Gathered FY16 Bookings Data...")
cnx.commit()

sql = "INSERT INTO master_bookings_data SELECT todays_bookings_data.* FROM todays_bookings_data"
mycursor.execute(sql)
cnx.commit()

cnx.close()