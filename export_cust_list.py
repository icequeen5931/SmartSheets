__author__ = 'jpisano'

import mysql.connector
from my_functions import stamp_it
import os
from settings import app,database

def export_cust_list(cust_seg,sales_level):

	download_file = app['DOWNLOAD_FILE']
	download_dir = app['DOWNLOAD_DIR']
	working_dir = app['WORKING_DIR']
	working_file = app['WORKING_FILE']
	working_data_dir = app['WORKING_DATA_DIR']
	as_of_date = app['AS_OF_DATE']

	try:
		os.remove(working_dir+working_data_dir+'Customer_List.csv')
	except:
		print ("No Existing Customer list")

	# this outputs the customer list in CVS format
	cnx = mysql.connector.connect(user=database['USER'], password=database['PASSWORD'], host=database['HOST'],
								  database=database['DATABASE'])
	mycursor = cnx.cursor()


	sql1 = ("(SELECT "
			"'End Customer Global Ultimate Name',"
			"'End Customer Global Ultimate Company Target ID',"
			"'Qty of N9300 PIDs ordered',"
			"'Qty of N9500 PIDs ordered',"
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

	if cust_seg == "*" :
		where_clause = ''
		cust_seg = 'ALL'
		sales_level = ''
	else:
		where_clause = "WHERE `Sales Level "+ sales_level + "` = '" + cust_seg +"' "

	sql2=(" UNION " + "(SELECT * FROM master_customer_data "+
		where_clause +
		"INTO OUTFILE '" + working_dir + working_data_dir + "Customer_List_" + cust_seg.replace(' ','_')+ ".csv' "
		"FIELDS ENCLOSED BY '\"' "
		"TERMINATED BY ',' "
		"ESCAPED BY '' "
		"LINES TERMINATED BY '\\r\\n');")

	sql = sql1 +  sql2
	mycursor.execute(sql)

	mycursor.execute("SELECT COUNT(*) FROM master_customer_data")
	current_customers = mycursor.fetchone()
	print("Master Customer Data: ", current_customers[0])

	stamp_it(working_dir + working_data_dir + "Customer_List_" + cust_seg.replace(' ','_')+ ".csv", as_of_date)
	cnx.commit()
	cnx.close()


if __name__ == "__main__":
	#Level 1
	# export_cust_list('Global Enterprise Theatre','1')
	#export_cust_list('GLOBAL SERVICE PROVIDER','1')
	# export_cust_list('APJ','1')
	# export_cust_list('Corp Adjustment','1')
	# export_cust_list('EMEAR-REGION','1')
	# export_cust_list('GREATER_CHINA','1')
	#
	# #Level 2
	export_cust_list('*','*')
	#export_cust_list('US COMMERCIAL','2')
	export_cust_list('US PS Market Segment','2')
	#export_cust_list('GLOBAL ENTERPRISE SEGMENT','2')
	#export_cust_list('US ENTERPRISE','2')




