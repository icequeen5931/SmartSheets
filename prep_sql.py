__author__ = 'jpisano'


import mysql.connector
from my_functions import table_exists
from settings import app,database

#
#
#
def prep_sql():
    cnx = mysql.connector.connect(user=database['USER'], password=database['PASSWORD'], host=database['HOST'], database=database['DATABASE'])
    mycursor = cnx.cursor()

    download_file = app['DOWNLOAD_FILE']
    download_dir = app['DOWNLOAD_DIR']
    working_dir = app['WORKING_DIR']
    working_file = app['WORKING_FILE']
    working_csv_file = app['WORKING_CSV_FILE']
    working_data_dir = app['WORKING_DATA_DIR']
    as_of_date = app['AS_OF_DATE']



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

    #Clean up old Bookings data
    if table_exists(mycursor,'master_bookings_data'):
        sql = "DROP TABLE master_bookings_data"
        mycursor.execute(sql)
        print("Deleted OLD Master Bookings Data...")
        cnx.commit()

    if table_exists(mycursor,'todays_bookings_data'):
        sql = "DROP TABLE todays_bookings_data"
        mycursor.execute(sql)
        print("Deleted Daily Bookings Data...")
        cnx.commit()

    #Create master_bookings table
    #
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

    #Make a duplicate for todays data
    #
    sql= "CREATE TABLE todays_bookings_data LIKE master_bookings_data;"
    mycursor.execute(sql)
    print("Created NEW Master Bookings Data...")
    cnx.commit()

    print("Importing NEW Bookings Data...")
    sql = ("load data local infile '" + working_dir+working_data_dir + working_csv_file + "' into table todays_bookings_data "
            "fields terminated by ',' "
            "enclosed by '\"' "
            "escaped by '' "
            "lines terminated by '\r\n' "
            "ignore 1 lines")
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


if __name__ == "__main__":
    prep_sql()