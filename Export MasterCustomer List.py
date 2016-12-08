__author__ = 'jpisano'

import mysql.connector
import os

os.remove('C:/Users/jpisano/Desktop/ACI to Production Database - Beta/Todays Data/Customer_List.csv')

# this outputs the customer list in CVS format
cnx = mysql.connector.connect(user='root', password='Wdst12498', host='localhost', database='cust_ref_db')
mycursor = cnx.cursor()

sql1 = ("(SELECT "
		"'End Customer Global Ultimate Name',"
		"'End Customer Global Ultimate Company Target ID',"
		"'Qty of N9300 PIDs ordered',"
		"'Qty of N9500 PIDs ordered',";
		"'Qty of APIC PIDs ordered',"
		"'Qty of C3 PIDs ordered',"
		"'Qty of NFM PIDs ordered',"
		"'Qty of Tetration PIDs ordered',"
		"'Sales Agent Name',"
		"'Assigned PSS',"
		"'Assigned TSA',"
		"'Reference Customer ?',"
		"'Target as ACI to Production by end of Q1 ?',"
		"'Equipment Status ?',"
		"'Next Steps',"
		"'Customer Vertical',"
		"'Target for Competitive Pursuit ?',"
		"'Other PSS',"
		"'Sales Level 1',"
		"'Sales Level 2',"
		"'Sales Level 3',"
		"'Sales Level 4',"
		"'Sales Level 5',"
		"'MultipleBookings',"
		"'FirstDateBooked',"
		"'LastDateBooked',"
		"'Last Refresh')" )

sql2=(" UNION " + "(SELECT * FROM cust_ref_db.master_customer_data "
	"INTO OUTFILE 'C:/Users/jpisano/Desktop/ACI to Production Database - Beta/Todays Data/Customer_List.csv' "
	"FIELDS ENCLOSED BY '\"' "
	"TERMINATED BY ',' "
	"ESCAPED BY '' "
	"LINES TERMINATED BY '\\r\\n');")

sql = sql1 + sql2

mycursor.execute(sql)
mycursor.execute("SELECT COUNT(*) FROM master_customer_data")
current_customers = mycursor.fetchone()
print("Master Customer Data: ", current_customers[0])

cnx.commit()
cnx.close()
