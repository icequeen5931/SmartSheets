__author__ = 'jpisano'
import xlrd
import datetime
import time
import mysql.connector
from os import sys

cnx=mysql.connector.connect(user='root',password='Wdst12498',host='localhost',database='cust_ref_db')
mycursor=cnx.cursor()

cnx1=mysql.connector.connect(user='root',password='Wdst12498',host='localhost',database='cust_ref_db')
mycursor1=cnx1.cursor()

#Load the Product ID list
mycursor.execute("SELECT * FROM product_ids")
product_ids = mycursor.fetchall()
var = mycursor.rowcount
print(var)

#Load the Coverage list
mycursor.execute("SELECT * FROM team_coverage")
team_coverage = mycursor.fetchall()
var = mycursor.rowcount
print(var)

#Loop through the fresh master_bookings_data and create a new Summary of master_customer_data
sql = "SELECT * FROM `master_bookings_data` ORDER BY master_bookings_data.`End Customer Global Ultimate Name`"
mycursor.execute(sql)
#master_bookings = mycursor.fetchall()
var = mycursor.rowcount
print(var)

#Load the first customer line item
customer_line_item = mycursor.fetchone()
cntr = 0
while customer_line_item is not None:

    for territory in team_coverage:
        tmp = (territory[2] + territory[3] + territory[4] + territory[5]+ territory[6]).strip()
        tmp_len = len(tmp)

        tmp1 = customer_line_item[5] + customer_line_item[6] + customer_line_item[7]+ customer_line_item[8]+ customer_line_item[9]

        if tmp1.startswith(tmp,0,tmp_len):
            pss = territory[0]
            tsa =  territory[1]
            print ("got a match:  ", pss,"  ",tsa,"   ",tmp)
            break
        else:
            print ("NO match:  ",tmp1)

    customer_line_item = mycursor.fetchone()
    cntr += 1
    print("sleeping  ", cntr)
    time.sleep(.5)

