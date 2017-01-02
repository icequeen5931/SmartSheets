__author__ = 'jpisano'

import mysql.connector
from settings import app,database

def create_master_customer_data():
    cnx = mysql.connector.connect(user=database['USER'], password=database['PASSWORD'], host=database['HOST'],
                                  database=database['DATABASE'])
    mycursor = cnx.cursor()

    cnx1 = mysql.connector.connect(user=database['USER'], password=database['PASSWORD'], host=database['HOST'],
                                  database=database['DATABASE'])
    mycursor1 = cnx1.cursor()


    mycursor.execute("SELECT COUNT(*) FROM master_customer_data")
    current_customers = mycursor.fetchone()
    print("Master Customer Data: ", current_customers[0])

    #sql = ("ALTER TABLE master_customer_data_as_of_1_2_2017 "
    #        "RENAME TO  master_customer_data_as_of_1_2_2017;")

    sql = "DROP TABLE master_customer_data"
    mycursor.execute(sql)
    print("Deleted OLD Master Customer Data...")
    cnx.commit()

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

    #Load the Team Coverage list
    mycursor.execute("SELECT * FROM coverage")
    team_coverage = mycursor.fetchall()

    #Load the Product ID list
    mycursor.execute("SELECT * FROM pids")
    product_ids = mycursor.fetchall()

    #Loop through the fresh master_bookings_data and create a new Summary of master_customer_data
    sql = ('SELECT * FROM `master_bookings_data` '
           'ORDER BY master_bookings_data.`End Customer Global Ultimate Name` ASC, `Date Booked` ASC')
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
        C3_PID = 0
        EMBRANE_PID = 0
        TETR_PID = 0

        #Look up PSS and TSA coverage for this customer
        pss = ''
        tsa = ''
        for territory in team_coverage:
            tmp = (territory[2] + territory[3] + territory[4] + territory[5] + territory[6]).strip()
            tmp = tmp.replace('*','')
            tmp_len = len(tmp)
            tmp1 = sales_lv1 + sales_lv2 + sales_lv3 + sales_lv4 + sales_lv5

            if tmp1.startswith (tmp, 0, tmp_len):
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
                    elif customer_line_item[14] == "C3":
                        C3_PID += 1
                    elif customer_line_item[14] == "EMBRANE":
                        EMBRANE_PID += 1
                    elif customer_line_item[14] == "TETR":
                        TETR_PID += 1

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