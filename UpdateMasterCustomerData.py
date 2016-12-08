__author__ = 'jpisano'

import mysql.connector

cnx = mysql.connector.connect(user='root', password='Wdst12498', host='localhost', database='cust_ref_db')
mycursor = cnx.cursor()

cnx1 = mysql.connector.connect(user='root', password='Wdst12498', host='localhost', database='cust_ref_db')
mycursor1 = cnx1.cursor()

#Loop through the fresh master_bookings_data and create a new Summary of master_customer_data
sql = ('SELECT * FROM `smartsheet` '
       'ORDER BY smartsheet.`End Customer Global Ultimate Name` ASC')
mycursor.execute(sql)

#Loop through each of the existing smartsheet data table
#Load the first customer line item
smartsheet_customer_line_item = mycursor.fetchone()

progress = 0
rec_cnt = 0

while smartsheet_customer_line_item is not None:
       #Look up the Customer in the SmartSheet
       # Init per customer counters and variables
       smartsheet_customer_name= smartsheet_customer_line_item[0]


       sql = "SELECT * FROM master_customer_data WHERE `End Customer Global Ultimate Name`= " + "'" + smartsheet_customer_name + "'"
       print (sql)
       mycursor1.execute(sql)
       #customer_name = mycursor1.fetchone()
       #print (smartsheet_customer_name)
       print (smartsheet_customer_name)
       #Get the next SmartSheet Entry
       smartsheet_customer_line_item = mycursor.fetchone()




