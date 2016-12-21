__author__ = 'jpisano'
import xlrd
import csv
import hashlib
import datetime
import os
import zipfile

# a change
def csv_from_excel(working_dir,working_file):
    #This function reads an excel sheet and creates a CSV file

    your_csv_file = open(''.join([working_dir + working_file.replace(".xlsx",""), '.csv']), 'w',newline='')
    print ('Your CSV file: ',your_csv_file)
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    wb= xlrd.open_workbook(working_dir + working_file)
    print("Workbook Opened: ",working_file)

    ws = wb.sheets()

    for sheet in ws:
        rows = sheet.get_rows()
        row_idx = -1
        for row in rows :
            output_row = []
            row_string = ''
            row_idx += 1

            for cell in row:
                value = cell.value
                if cell.ctype == xlrd.XL_CELL_DATE :
                    # 61 is the lowest Excel Date we can have due to leap year issues
                    if value < 61:
                        value = 61
                    tmp_date = datetime.datetime(*xlrd.xldate_as_tuple(value, wb.datemode))
                    value = tmp_date.strftime('%Y/%m/%d')

                if cell.ctype == xlrd.XL_CELL_TEXT :
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
    sql = "SELECT * FROM information_schema.tables WHERE table_name = '"+ tbl_name + "'"
    mycursor.execute(sql)
    if mycursor.fetchone() != None:
        return True
    else:
        return False

def get_new_zip_file(download_dir, download_file, working_dir, working_file,timestamp):
    # Is there a bookings file downloaded ?
    if os.path.exists(download_dir + download_file):

        # Does the working file exist ? if so let's rename it
        if os.path.exists(working_dir):
            try:
                #Rename and timestamp the existing  file
                base_name = os.path.splitext(working_file)[0]
                ext_name = os.path.splitext(working_file)[1]
                os.rename(working_dir + working_file, working_dir + base_name + timestamp + ext_name)
                print()
                print("Previous bookings data renamed to: " + base_name + timestamp + ext_name)
            except FileNotFoundError as err:
                print()
                print("Just FYI - No existing file to rename")

            #Unzip the file into the specified path
            zip_ref = zipfile.ZipFile(download_dir + download_file)
            zip_ref.extractall(working_dir)

            # close out the zip file
            zip_ref.close()

            #timestamp and rename the downloaded bookings file
            base_name = os.path.splitext(download_file)[0]
            ext_name = os.path.splitext(download_file)[1]
            os.rename(download_dir + download_file, download_dir +base_name + timestamp + ext_name)
            print()
            print("New Bookings Data File Ready !")
    else:
        print()
        print('Bookings Data not yet downloaded. Please download current copy !')
