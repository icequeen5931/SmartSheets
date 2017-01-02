__author__ = 'jpisano'


import xlrd
import csv
import hashlib
import datetime
import os
import zipfile

def csv_from_excel(working_file,sheet_name):
    #This function reads an excel sheet and creates a CSV file

    your_csv_file = open(''.join([working_file.replace(".xlsm",""), '.csv']), 'w',newline='')
    print ('Your CSV file: ',your_csv_file.name)
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    print()
    print("Opening Workbook: ", working_file)
    wb= xlrd.open_workbook(working_file)
    print("Workbook Opened: ",working_file)

    ws = wb.sheets()

    for sheet in ws:
        if sheet.name == sheet_name:
            print("Processing sheet: ",sheet_name)
            rows = sheet.get_rows()
            row_idx = -1
            for row in rows :
                output_row = []
                row_string = ''
                row_idx += 1

                for cell in row:
                    value = cell.value
                    if cell.ctype == xlrd.XL_CELL_DATE:
                        # 61 is the lowest Excel Date we can have due to leap year issues
                        if value < 61:
                            value = 61
                        tmp_date = datetime.datetime(*xlrd.xldate_as_tuple(value, wb.datemode))
                        value = tmp_date.strftime('%Y/%m/%d')

                    if cell.ctype == xlrd.XL_CELL_TEXT:
                        # Strip out Unicode characters above value 127
                        # Make it all ASCII
                        cell_bytes = (cell.value).encode('ascii','ignore')
                        value =cell_bytes.decode('utf-8')

                    #Add this cell value to the output row list
                    row_string = row_string + str(value)
                    output_row.append(value)

                # Add the Hash Value for this output_row
                if row_idx == 0:
                    output_row.append('HashVal')
                else:
                    output_row.append(hashlib.md5(row_string.encode('utf-8')).hexdigest())

                # Write the output_row list to the CSV file
                wr.writerow([(entry) for entry in output_row])

            #Close up the CSV file and exit
            your_csv_file.close()


def table_exists(mycursor,tbl_name):
    sql = "SELECT * FROM information_schema.tables WHERE table_name = '" + tbl_name + "'"
    mycursor.execute(sql)
    if mycursor.fetchone() != None:
        return True
    else:
        return False


def stamp_it(working_file,timestamp):
    # Timestamp and rename the working file
    base_name = os.path.splitext(working_file)[0]
    ext_name = os.path.splitext(working_file)[1]
    # add a H/M/S extension if it already exists
    if os.path.exists(base_name + timestamp + ext_name):
        add_ext = datetime.datetime.now()
        os.rename(working_file,base_name + timestamp + add_ext.strftime('_%H_%M_%S') + ext_name)
    else:
        print (working_file,base_name,ext_name)
        os.rename(working_file, base_name + timestamp + ext_name)

def get_new_zip_file(source_file,dest_file):
    #Unzip the file into the specified path
    zip_ref = zipfile.ZipFile(source_file)
    zip_ref.extractall(dest_file)

    # close out the zip file
    zip_ref.close()
