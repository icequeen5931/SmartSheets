import mysql.connector

cnx=mysql.connector.connect(user='root',password='Wdst12498',host='localhost',database='cust_ref_db')
mycursor=cnx.cursor()

cnx1=mysql.connector.connect(user='root',password='Wdst12498',host='localhost',database='cust_ref_db')
mycursor1=cnx1.cursor()

mycursor.execute("SHOW TABLES")
print (mycursor.fetchall())

#Loop through the fresh master_bookings_data and create a new Summary of master_customer_data
sql = ('SELECT * FROM `tue_data`'
       'ORDER BY tue_data.`End Customer Global Ultimate Name` ASC, `Date Booked` DESC')

#sql = ("SELECT  tue_data.`Hash Value` AS TUE_HASH,"
#    "tue_data.`End Customer Global Ultimate Name` AS TUE_CUST,"
#    "wed_data.`Hash Value` AS WED_HASH,"
#    "wed_data.`End Customer Global Ultimate Name` AS WED_CUST "
#    "FROM tue_data INNER JOIN wed_data "
#    "on tue_data.`Hash Value` = wed_data.`Hash Value` ")
mycursor.execute(sql)

#sql = ('SELECT * FROM `wed_data`'
      # 'ORDER BY wed_data.`End Customer Global Ultimate Name` ASC, `Date Booked` DESC')
#mycursor1.execute(sql)
#print(mycursor1.rowcount)

x=0

#Load the first customer line item
customer_line_item = mycursor.fetchone()

while customer_line_item is not None:
#while x < 20:

    hash_val = customer_line_item[0]
    current_customer = customer_line_item[1]
    current_customer_id = customer_line_item[2]
    #print (x,hash_val,current_customer,current_customer_id)
    #x = x + 1

    #hash_val = "091db10c182953afb871d6d7e11b2634"
    # Look in Wed data for this hash
    sql = ("SELECT * FROM `wed_data` WHERE `Hash Value` = " + "'" + hash_val + "'")
    #print(sql)

    mycursor1.execute(sql)
    wed_data = mycursor1.fetchone()
    if wed_data is None :
        x = x+1

        print('NOT Found: ', hash_val)
        #print (wed_data[0])
    #print("Results --->  ", mycursor1.fetchone())

    # Get the next bookings line item
    customer_line_item = mycursor.fetchone()



print ("Customers NOT found in Wed = ",x)
#cnx.commit()
cnx.close()

#cnx1.commit()
cnx1.close()