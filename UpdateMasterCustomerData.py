__author__ = 'jpisano'

import mysql.connector

#This program takes the most current SmartSheet data and updates the master_customer_data table

cnx = mysql.connector.connect(user='root', password='Wdst12498', host='localhost', database='cust_ref_db')
mycursor = cnx.cursor()

cnx1 = mysql.connector.connect(user='root', password='Wdst12498', host='localhost', database='cust_ref_db')
mycursor1 = cnx1.cursor(buffered=True)
#mycursor1 = cnx1.cursor()

#Loop through the current downloaded smartsheet this will be the main loop
sql = ('SELECT * FROM `smartsheet` '
       'ORDER BY smartsheet.`End Customer Global Ultimate Name` ASC')
mycursor.execute(sql)

#Load the first customer in the smartsheet line item
smartsheet_customer_line_item = mycursor.fetchone()

progress = 0
rec_cnt = 0

while smartsheet_customer_line_item is not None:
       #Look up the Customer in the SmartSheet
       # Init per customer variables
       smartsheet_customer_name= smartsheet_customer_line_item[0]

       smartsheet_ref_cust =  smartsheet_customer_line_item[8] #Reference Customer ?
       smartsheet_aci_prod =  smartsheet_customer_line_item[9] #Target as ACI to Production by end of Q1 ?
       smartsheet_cust_stat =  smartsheet_customer_line_item[10] #Equipment Status ?
       smartsheet_next_steps =  smartsheet_customer_line_item[11] #Next Steps
       smartsheet_cust_vertical = smartsheet_customer_line_item[12]  # Customer Vertical
       smartsheet_comp_pursuit = smartsheet_customer_line_item[13]  # Target for Comp Pursuit

       # This is all very silly we need to strip these characters out to make sql work
       #Need a better way
       smartsheet_ref_cust =  smartsheet_ref_cust.replace("'", " ")
       smartsheet_aci_prod =  smartsheet_aci_prod.replace("'", " ")
       smartsheet_cust_stat =  smartsheet_cust_stat.replace("'", " ")
       smartsheet_next_steps =  smartsheet_next_steps.replace("'", " ")
       smartsheet_cust_vertical = smartsheet_cust_vertical.replace("'", " ")
       smartsheet_comp_pursuit = smartsheet_comp_pursuit.replace("'", " ")

       smartsheet_ref_cust =  smartsheet_ref_cust.replace('"', " ")
       smartsheet_aci_prod =  smartsheet_aci_prod.replace('"', " ")
       smartsheet_cust_stat =  smartsheet_cust_stat.replace('"'," ")
       smartsheet_next_steps =  smartsheet_next_steps.replace('"', " ")
       smartsheet_cust_vertical = smartsheet_cust_vertical.replace('"', " ")
       smartsheet_comp_pursuit = smartsheet_comp_pursuit.replace('"', " ")

       smartsheet_ref_cust =  smartsheet_ref_cust.replace(',', " ")
       smartsheet_aci_prod =  smartsheet_aci_prod.replace(',', " ")
       smartsheet_cust_stat =  smartsheet_cust_stat.replace(','," ")
       smartsheet_next_steps =  smartsheet_next_steps.replace(',', " ")
       smartsheet_cust_vertical = smartsheet_cust_vertical.replace(',', " ")
       smartsheet_comp_pursuit = smartsheet_comp_pursuit.replace(',', " ")

       smartsheet_ref_cust =  smartsheet_ref_cust.replace('\\', " ")
       smartsheet_aci_prod =  smartsheet_aci_prod.replace('\\', " ")
       smartsheet_cust_stat =  smartsheet_cust_stat.replace('\\'," ")
       smartsheet_next_steps =  smartsheet_next_steps.replace('\\', " ")
       smartsheet_cust_vertical = smartsheet_cust_vertical.replace('\\', " ")
       smartsheet_comp_pursuit = smartsheet_comp_pursuit.replace('\\', " ")

       sql = "SELECT * FROM master_customer_data WHERE `End Customer Global Ultimate Name`= " + '"' + smartsheet_customer_name + '"'
       mycursor1.execute(sql)

       if mycursor1.rowcount == 0 :
              #Handle error here if we don't find the customer
              print ("None found: ", smartsheet_customer_name, mycursor1.rowcount)
              print(sql)
       elif mycursor1.rowcount > 1:
              # Handle error here if we find more than one customer
              print("More than one: ",smartsheet_customer_name, mycursor1.rowcount)
              print(sql)
       else:
              print (smartsheet_customer_name)
              sql= ('UPDATE master_customer_data '
                     'SET `Reference Customer ?` = ' + '"' + smartsheet_ref_cust + '", '
                     '`Target as ACI to Production by end of Q1 ?` = ' + '"' + smartsheet_aci_prod + '", '
                     '`Equipment Status ?` = ' + '"' + smartsheet_cust_stat + '", '
                     '`Next Steps` = ' + '"' + smartsheet_next_steps + '", '
                     '`Customer Vertical` = ' + '"' + smartsheet_cust_vertical + '", '
                     '`Target for Competitive Pursuit ?` = ' + '"' + smartsheet_comp_pursuit + '" '
                     'WHERE `End Customer Global Ultimate Name` = ' + '"' + smartsheet_customer_name + '"') #Don't changes these quotes in case the customer name contains an apostophre
              #print (sql)
              mycursor1.execute(sql)

       smartsheet_customer_line_item = mycursor.fetchone()




cnx1.commit()

cnx.close()
cnx1.close()

