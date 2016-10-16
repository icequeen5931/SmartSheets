__author__ = 'jpisano'

import mysql.connector

cnx=mysql.connector.connect(user='root',password='Wdst12498',host='localhost',database='ref_db')
#cnx=mysql.connector.connect(user='root',password='Wdst12498',host='customerdb.cp1kaaiuayns.us-east-1.rds.amazonaws.com',database='ref_db')

mycursor=cnx.cursor()

mycursor.execute("SHOW TABLES")
print (mycursor.fetchall())

#mycursor.execute("ALTER TABLE current_data ADD COLUMN Status VARCHAR(45) NULL AFTER `Bookings Adjustments Description`")
#mycursor.execute("SELECT * FROM current_data")
#rows = mycursor.fetchall()
#print (rows)
#fy15 = 0
#fy16 = 0
#for row in rows:
 #   if row[1] == "2015":
  #      fy15 = fy15+1
   # if row[1] == "2016":
    #    fy16 = fy16+1

#print ("FY15 Bookings",fy15)
#print ("FY16 Bookings",fy16)

#mycursor.execute("SELECT COUNT(*) FROM current_data")
#print(mycursor.fetchone())

#mycursor.execute ("CREATE SCHEMA blanche")
#mycursor.query('DROP DATABASE test')
#mycursor.query('CREATE DATABASE test')
#mycursor.query("GRANT ALL ON test.* to ''@'localhost'")
#mycursor.execute("""drop table if exists towns""")
#mycursor.execute("""drop table if exists hotels""")
#mycursor.execute("DROP TABLE IF EXISTS stanley")

mycursor.execute("SELECT VERSION()")
print (mycursor.fetchall())

#mycursor.execute("CREATE TABLE stanley ()")
#mycursor.execute("CREATE TABLE stanley(Name VARCHAR(25))")

#mycursor.execute("CREATE TABLE stanley(Id INT PRIMARY KEY AUTO_INCREMENT,Name VARCHAR(25))")
#print (mycursor.fetchall())


cnx.commit()
cnx.close()