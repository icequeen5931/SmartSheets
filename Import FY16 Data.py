__author__ = 'jpisano'

import mysql.connector

cnx = mysql.connector.connect(user='root', password='Wdst12498', host='localhost', database='cust_ref_db')
mycursor = cnx.cursor()

cnx1 = mysql.connector.connect(user='root', password='Wdst12498', host='localhost', database='cust_ref_db')
mycursor1 = cnx1.cursor()

# path_to_import = 'c:/users/jpisano/desktop/ACI to Production Database/Todays Data/'
# file_to_import = 'fy16_bookings_data.csv'

#Check Table Sizes
# mycursor.execute("SELECT COUNT(*) FROM fy15_bookings_data")
# print("fy15 Bookings Data: ", mycursor.fetchone())
#
# mycursor.execute("SELECT COUNT(*) FROM fy16_bookings_data")
# print("fy16 Bookings Data: ",  mycursor.fetchone())
#
# mycursor.execute("SELECT COUNT(*) FROM master_bookings_data")
# print("Master Bookings Data: ", mycursor.fetchone())
#
mycursor.execute("SELECT COUNT(*) FROM master_customer_data")
current_customers = mycursor.fetchone()
print("Master Customer Data: ", current_customers[0])
#
# mycursor.execute("SELECT COUNT(*) FROM prev_master_customer_data")
# print("Previous Master Customer Data: ",  mycursor.fetchone())

#Clean out the FY16 table and master bookings data
# mycursor.execute("DELETE FROM fy16_bookings_data")
# cnx.commit()
#mycursor.execute("DELETE FROM master_bookings_data")
#cnx.commit()

#Add in fresh Bookings Data
# full_path = path_to_import + file_to_import
# sql = ("LOAD DATA LOCAL INFILE " + "'" + full_path + "'"
#        " INTO TABLE fy16_bookings_data FIELDS TERMINATED BY ','"
#        " ENCLOSED BY '" + '"' + "' ESCAPED BY " + "'" + "'"
#        " LINES TERMINATED BY '" + "\r\n" + "'")
# mycursor.execute(sql)
# cnx.commit()

#INSERT fy15_bookings into the master
# sql = ('INSERT INTO master_bookings_data'
#        ' SELECT fy15_bookings_data.* FROM fy15_bookings_data')
# mycursor.execute(sql)
# cnx.commit()

#INSERT fy16_bookings into the master
# sql = ('INSERT INTO master_bookings_data'
#        ' SELECT fy16_bookings_data.* FROM fy16_bookings_data')
# mycursor.execute(sql)
# cnx.commit()

#Backup and copy master_customer_data to prev_master_customer_data
# mycursor.execute('DELETE FROM prev_master_customer_data')
# cnx.commit()
# sql = "INSERT prev_master_customer_data SELECT * FROM master_customer_data"
# mycursor.execute(sql)
# cnx.commit()

#Clean out the Master Customer Data table
#mycursor.execute("DELETE FROM master_customer_data")
#cnx.commit()

#Load the Team Coverage list
mycursor.execute("SELECT * FROM team_coverage")
team_coverage = mycursor.fetchall()

#Load the Product ID list
mycursor.execute("SELECT * FROM product_ids")
product_ids = mycursor.fetchall()

#Loop through the fresh master_bookings_data and create a new Summary of master_customer_data
sql = ('SELECT * FROM `master_bookings_data` '
       'ORDER BY master_bookings_data.`End Customer Global Ultimate Name` ASC, `Date Booked` DESC')
mycursor.execute(sql)

#Loop through each of the master_bookings_data table
#Load the first customer line item
customer_line_item = mycursor.fetchone()

progress = 0
rec_cnt = 0

while customer_line_item is not None:

    # Init per customer counters and variables
    current_customer = customer_line_item[16]
    current_customer_id = customer_line_item[17]
    first_date_booked = customer_line_item[4]
    account_mgr = customer_line_item[11]
    sales_lv1 = customer_line_item[5]
    sales_lv2 = customer_line_item[6]
    sales_lv3 = customer_line_item[7]
    sales_lv4 = customer_line_item[8]
    sales_lv5 = customer_line_item[9]
    n9300_PID = 0
    n9500_PID = 0
    APIC_PID = 0

    #Look up PSS and TSA coverage for this customer
    pss = ''
    tsa = ''
    for territory in team_coverage:
        tmp = (territory[2] + territory[3] + territory[4] + territory[5] + territory[6]).strip()
        tmp_len = len(tmp)
        tmp1 = sales_lv1 + sales_lv2 + sales_lv3 + sales_lv4 + sales_lv5

        if tmp1.startswith(tmp, 0, tmp_len):
            pss = territory[0]
            tsa = territory[1]
            break

    #Loop through this customers bookings data until we get to the next customer
    while current_customer == customer_line_item[16]:

        #Last Date Booked
        last_date_booked = customer_line_item[4]

        #See if this product ID is interesting
        #We only count "interesting" PIDs
        for product_id in product_ids:
            if product_id[1] == customer_line_item[15]:
                #Capture PID totals
                if customer_line_item[14] == "N9300":
                    n9300_PID += 1
                elif customer_line_item[14] == "N9500":
                    n9500_PID += 1
                elif customer_line_item[14] == "APIC":
                    APIC_PID += 1

        #Get the next bookings line item
        rec_cnt = rec_cnt + 1
        customer_line_item = mycursor.fetchone()

        #Kick out if this is the last item
        if customer_line_item is None:
            break

    #Kick out if this is the last item
    if customer_line_item is None:
        break

    #Create a customer record
    sql = (
        'INSERT INTO master_customer_data '
        ' (`End Customer Global Ultimate Name`,'
        ' `End Customer Global Ultimate Company Target ID`,'
        ' `Qty of N9300 PIDs ordered`,'
        ' `Qty of N9500 PIDs ordered`,'
        ' `Qty of APIC PIDs ordered`,'
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
        '"' + first_date_booked + '",'  # First Date Booked
        '"' + last_date_booked + '",'  # Last Date Booked
        '"Last Refresh")')

    mycursor1.execute(sql)
    cnx1.commit()

    progress = progress + 1
    if progress%1000 == 0:
            print ("Customer Processed: ", progress)

cnx.commit()

# print out some stats
mycursor1.execute("SELECT COUNT(*) FROM master_customer_data")
new_customers = mycursor1.fetchone()
print("Bookings Records Processed: ",rec_cnt)
print("Master Customer Data: ", new_customers[0])
print("We have added: " + str(new_customers[0] - current_customers[0]) + " customers")

#Clean up and Close out
cnx.close()
cnx1.close()