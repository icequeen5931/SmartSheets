__author__ = 'jpisano'

import mysql.connector

# this outputs the customer list in CVS format
cnx = mysql.connector.connect(user='root', password='Wdst12498', host='localhost', database='cust_ref_db')
mycursor = cnx.cursor()

sql = ("SELECT * FROM cust_ref_db.master_customer_data "
	"INTO OUTFILE 'C:/Users/jpisano/Desktop/ACI to Production Database - Beta/Todays Data/Customer_List.csv' "
	"FIELDS ENCLOSED BY '\"' "
	"TERMINATED BY ',' "
	"ESCAPED BY '' "
	"LINES TERMINATED BY '\\r\\n';")

mycursor.execute(sql)
mycursor.execute("SELECT COUNT(*) FROM master_customer_data")
current_customers = mycursor.fetchone()
print("Master Customer Data: ", current_customers[0])

cnx.commit()
cnx.close()