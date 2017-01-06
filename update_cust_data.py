__author__ = 'jpisano'

import mysql.connector
from settings import app,database

def update_cust_data():
       #This program takes the most current SmartSheet data and updates the master_customer_data table
       #
       # Create 2 mySQL connections
       cnx = mysql.connector.connect(user=database['USER'], password=database['PASSWORD'], host=database['HOST'],
                                     database=database['DATABASE'])
       mycursor = cnx.cursor()

       cnx1 = mysql.connector.connect(user=database['USER'], password=database['PASSWORD'], host=database['HOST'],
                                      database=database['DATABASE'])
       mycursor1 = cnx1.cursor()

       #Loop through the current downloaded smartsheet this will be the main loop
       sql = ('SELECT * FROM `smartsheet` '
              'ORDER BY smartsheet.`End Customer Global Ultimate Name` ASC')
       mycursor.execute(sql)

       #Load the first customer in the smartsheet line item
       smartsheet_customer_line_item = mycursor.fetchone()

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

              sql = "SELECT * FROM master_customer_data WHERE `End Customer Global Ultimate Name` = %s"
              query_values = (smartsheet_customer_name,)
              mycursor1.execute(sql, query_values)

              if mycursor1.rowcount == 0 :
                     #Handle error here if we don't find the customer
                     print ("None found: ", smartsheet_customer_name, mycursor1.rowcount)
              elif mycursor1.rowcount > 1:
                     # Handle error here if we find more than one customer
                     print("More than one: ",smartsheet_customer_name, mycursor1.rowcount)
                     print(sql)
              else:
                     sql= ("UPDATE master_customer_data "
                            "SET `Reference Customer ?` = %s, "
                            "`Target as ACI to Production by end of Q1 ?` =  %s, "
                            "`Equipment Status ?` =  %s, "
                            "`Next Steps` =  %s, "
                            "`Customer Vertical` =  %s, "
                            "`Target for Competitive Pursuit ?` =  %s "
                            "WHERE `End Customer Global Ultimate Name` =  %s")

                     query_values = (smartsheet_ref_cust, smartsheet_aci_prod, smartsheet_cust_stat,
                                     smartsheet_next_steps, smartsheet_cust_vertical, smartsheet_comp_pursuit,
                                     smartsheet_customer_name)
                     mycursor1.execute(sql,query_values)

              #Go get the next Customer
              smartsheet_customer_line_item = mycursor.fetchone()

       # Clean up and Exit
       cnx1.commit()
       cnx.close()
       cnx1.close()

if __name__ == "__main__":
    update_cust_data()