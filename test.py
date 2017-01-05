__author__ = 'jpisano'

import mysql.connector
from my_functions import table_exists
from settings import app,database
from Coverage import Coverage
from datetime import datetime
from datetime import date
import time

cnx = mysql.connector.connect(user=database['USER'], password=database['PASSWORD'], host=database['HOST'],
                              database=database['DATABASE'])
mycursor = cnx.cursor()

cnx1 = mysql.connector.connect(user=database['USER'], password=database['PASSWORD'], host=database['HOST'],
                              database=database['DATABASE'])
mycursor1 = cnx1.cursor()

#Delete and re-create master customer data as required
if table_exists(mycursor, 'master_customer_data'):
    mycursor.execute("SELECT COUNT(*) FROM master_customer_data")
    current_customers = mycursor.fetchone()
    print("Master Customer Data: ", current_customers[0])

    sql = "DROP TABLE master_customer_data"
    mycursor.execute(sql)
    print("Deleted OLD Master Customer Data...")
    cnx.commit()
else:
    current_customers = [0, ]

sql = ('CREATE TABLE master_customer_data ('
       '`End Customer Global Ultimate Name` TEXT,'
       '`End Customer Global Ultimate Company Target ID` TEXT,'
       '`Qty of N9300 PIDs ordered` TEXT,'
       '`Qty of N9500 PIDs ordered` TEXT,'
       '`Qty of APIC PIDs ordered` TEXT,'
       '`Qty of C3 PIDs ordered` TEXT,'
       '`Qty of NFM PIDs ordered` TEXT,'
       '`Qty of Tetration PIDs ordered` TEXT,'
       '`Sales Agent Name` TEXT,'
       '`Assigned PSS` TEXT,'
       '`Assigned TSA` TEXT,'
       '`Reference Customer ?` TEXT,'
       '`Target as ACI to Production by end of Q1 ?` TEXT,'
       '`Equipment Status ?` TEXT,'
       '`Next Steps` TEXT,'
       '`Customer Vertical` TEXT,'
       '`Target for Competitive Pursuit ?` TEXT,'
       '`Other PSS` TEXT,'
       '`Sales Level 1` TEXT,'
       '`Sales Level 2` TEXT,'
       '`Sales Level 3` TEXT,'
       '`Sales Level 4` TEXT,'
       '`Sales Level 5` TEXT,'
       '`MultipleBookings` TEXT,'
       '`FirstDateBooked` DATE,'
       '`LastDateBooked` DATE,'
       '`Last Refresh` TEXT)')
mycursor.execute(sql)
cnx.commit()

# Load the Product ID list and then create two dicts (one by ProdID and one by ProdFam)
mycursor.execute("SELECT * FROM pids")
products = mycursor.fetchall()

prod_id_dict = {}
prod_fam_dict ={}
for product in products:
    prod_id_dict[product[1]] = (product[0],product[2])
    prod_fam_dict[product[0]]= (product[1],product[2])
print(prod_fam_dict.keys())
print(prod_id_dict)

#Get each unique Customer Name
sql = ('SELECT DISTINCT `End Customer Global Ultimate Name` FROM `master_bookings_data`'
       'ORDER BY `End Customer Global Ultimate Name` ASC')

mycursor.execute(sql)
customers = mycursor.fetchall()

print ("Customers Found: ",len(customers))

# Create a the Team Coverage Object
my_coverage = Coverage()

print ('start',datetime.now())
for customer in customers:

    #Gather this customers orders
    sql = "SELECT * FROM `master_bookings_data` WHERE `End Customer Global Ultimate Name` = %s"
    query_values = (customer)
    mycursor.execute(sql,query_values)
    orders = mycursor.fetchall()

    # Init per customer counters and variables
    n9300_PID = 0
    n9500_PID = 0
    APIC_PID = 0
    C3_PID = 0
    EMBRANE_PID = 0
    TETR_PID = 0
    pss = ''
    tsa = ''
    first_date_booked = date(2030, 3, 1) #Random Date in the future
    last_date_booked = date(1900, 3, 1) #Default earliest date for Excel

    for order in orders:
        # Init per customer counters and variables
        current_customer = order[16]
        current_customer_id = order[17]
        account_mgr = order[11]

        # Set the first and last date booked
        if first_date_booked > order[4]:
            first_date_booked = order[4]
        if last_date_booked < order[4]:
            last_date_booked = order[4]

        # Do we count this PID ? If not skip it
        # order[14] has ProdFam,  order[15] has ProdID
        if order[14] == "TETR":
            TETR_PID += 1
        elif order[14] == "C3":
            C3_PID += 1
        elif prod_id_dict.get(order[15]) is not None:
            #print('FOUND  Product ID: ',order[15])
            if prod_id_dict[order[15]][0] == 'N9300':
                n9300_PID += 1
            elif prod_id_dict[order[15]][0] == 'N9500':
                n9500_PID += 1
            elif prod_id_dict[order[15]][0] == 'APIC':
                APIC_PID += 1
            elif prod_id_dict[order[15]][0] == 'EMBRANE':
                EMBRANE_PID += 1
        else:
            continue # Get the next order since this is not interesting

        # Get the territory this booked in
        sales_lv1 = order[5]
        sales_lv2 = order[6]
        sales_lv3 = order[7]
        sales_lv4 = order[8]
        sales_lv5 = order[9]
        sales_str = order[5]+order[6]+order[7] +order[8] +order[9]

        #Find the team(s) that cover this customer in this territory
        teams = my_coverage.find_team(sales_str)
        pss = pss + ' '.join(teams[0])
        tsa = tsa + ' '.join(teams[1])

    # We are done with this customer
    # Create a summary customer record
    sql = (
        'INSERT INTO master_customer_data '
        ' (`End Customer Global Ultimate Name`,'
        ' `End Customer Global Ultimate Company Target ID`,'
        ' `Qty of N9300 PIDs ordered`,'
        ' `Qty of N9500 PIDs ordered`,'
        ' `Qty of APIC PIDs ordered`,'
        ' `Qty of C3 PIDs ordered`,'
        ' `Qty of NFM PIDs ordered`,'
        ' `Qty of Tetration PIDs ordered`,'
        ' `Sales Agent Name`,'
        ' `Assigned PSS`,'
        ' `Assigned TSA`,'
        ' `Reference Customer ?`,'
        ' `Target as ACI to Production by end of Q1 ?`,'
        ' `Equipment Status ?`,'
        ' `Next Steps`,'
        ' `Customer Vertical`,'
        ' `Target for Competitive Pursuit ?`,'
        ' `Other PSS`,'
        ' `Sales Level 1`,'
        ' `Sales Level 2`,'
        ' `Sales Level 3`,'
        ' `Sales Level 4`,'
        ' `Sales Level 5`,'
        ' `MultipleBookings`,'
        ' `FirstDateBooked`,'
        ' `LastDateBooked`,'
        ' `Last Refresh`)'
        ' VALUES'
        ' ("' + current_customer + '",'
        '"' + current_customer_id + '",'
        '"' + str(n9300_PID) + '",'
        '"' + str(n9500_PID) + '",'
        '"' + str(APIC_PID) + '",'
        '"' + str(C3_PID) + '",'
        '"' + str(EMBRANE_PID) + '",'
        '"' + str(TETR_PID) + '",'
        '"' + account_mgr + '",'
        '"' + pss + '",'  # Assigned PSS name
        '"' + tsa + '",'  # Assigned TSA name
        '"Reference Customer ?",'
        '"Target as ACI to Production by end of Q1",'
        '"Equipment Status ?",'
        '"Next Steps",'
        '"Customer Vertical",'
        '"Target for Competitive Pursuit ?",'
        '"Other PSS",'
        '"' + sales_lv1 + '",'  # Sales Level 1
        '"' + sales_lv2 + '",'  # Sales Level 2
        '"' + sales_lv3 + '",'  # Sales Level 3
        '"' + sales_lv4 + '",'  # Sales Level 4
        '"' + sales_lv5 + '",'  # Sales Level 5
        '"' + str(first_date_booked != last_date_booked) + '",'  # Multiple Bookings
        '"' + str(first_date_booked) + '",'  # First Date Booked
        '"' + str(last_date_booked) + '",'  # Last Date Booked
        '"Last Refresh")')

    mycursor1.execute(sql)
    cnx1.commit()

    #print('\t\t Customer: ',order[16])
    # print('\t\t\t\t Team: ',pss,' / ',tsa)
    # print('\t\t\t\t\t Region:',sales_str)
    # print('\t\t Products:',n9300_PID,n9500_PID,APIC_PID,EMBRANE_PID,C3_PID,TETR_PID)
    #print('========================================')
    #time.sleep(1)

#Clean up and Close out
cnx.close()
cnx1.close()

print('done !', datetime.now())




# Loop through each of the master_bookings_data table
# Load the first customer line item
#customer_line_item = mycursor.fetchone()
#
# progress = 0
# rec_cnt = 0
# print ("start")
# while customer_line_item is not None:
#     # Init per customer counters and variables
#     current_customer = customer_line_item[16]
#     current_customer_id = customer_line_item[17]
#     first_date_booked = customer_line_item[4]
#     account_mgr = customer_line_item[11]
#     sales_lv1 = customer_line_item[5]
#     sales_lv2 = customer_line_item[6]
#     sales_lv3 = customer_line_item[7]
#     sales_lv4 = customer_line_item[8]
#     sales_lv5 = customer_line_item[9]
#     n9300_PID = 0
#     n9500_PID = 0
#     APIC_PID = 0
#     C3_PID = 0
#     EMBRANE_PID = 0
#     TETR_PID = 0
#
#     print(rec_cnt,current_customer,'\t\t',sales_lv1,sales_lv2,sales_lv3,sales_lv4,sales_lv5)
#     time.sleep(.25)
#
#     rec_cnt = rec_cnt+1
#     customer_line_item = mycursor.fetchone()
#
# print ("Done !")