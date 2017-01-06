__author__ = 'jpisano'

import mysql.connector
from my_functions import stamp_it
from settings import app,database
from datetime import datetime

def export_cust_list(customer_lists):
    start_time = datetime.now()
    print('\texport_cust_list started: ', datetime.now())

    # this outputs the customer list in CVS format
    cnx = mysql.connector.connect(user=database['USER'],
                                  password=database['PASSWORD'],
                                  host=database['HOST'],
                                  database=database['DATABASE'])
    mycursor = cnx.cursor()

    for customer_list in customer_lists:
        cust_seg = customer_list[0]
        sales_level = customer_list[1]

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
            "INTO OUTFILE '" + app['WORKING_DIR'] + app['WORKING_DATA_DIR'] +
            "Customer_List_" + cust_seg.replace(' ','_')+ ".csv' "
            "FIELDS ENCLOSED BY '\"' "
            "TERMINATED BY ',' "
            "ESCAPED BY '' "
            "LINES TERMINATED BY '\\r\\n');")

        sql = sql1 +  sql2
        mycursor.execute(sql)

        stamp_it(app['WORKING_DIR'] + app['WORKING_DATA_DIR'] +
                 "Customer_List_" + cust_seg.replace(' ','_')+ ".csv", app['AS_OF_DATE'])
        cnx.commit()

    cnx.close()

    end_time = datetime.now()
    print ('\t\trun time: ', end_time - start_time)
    print ('\texport_cust_list complete: ',datetime.now())



if __name__ == "__main__":
    customer_lists = [('*','*'),
                  ('US COMMERCIAL', '2'),
                  ('US PS Market Segment', '2'),
                  ('GLOBAL ENTERPRISE SEGMENT', '2'),
                  ('US ENTERPRISE', '2'),
                  ('APJ', '1')]
    export_cust_list(customer_lists)





