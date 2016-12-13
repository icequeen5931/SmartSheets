__author__ = 'jpisano'
import xlrd
import csv
import hashlib
import datetime

# a change

def csv_from_excel(path_to_import,file_to_import):
    #This function reads an excel sheet and creates a CSV file
    excel_file = path_to_import + file_to_import
    print ("Opening Workbook")
    workbook = xlrd.open_workbook(excel_file)
    print ("Workbook Opened")

    #xlrd.dump(excel_file,ijm)
    all_worksheets = workbook.sheet_names()
    #print ("Sheets - >>>>  ",all_worksheets)
    print(workbook.nsheets)

    #Loop through all the worksheets
    for worksheet_name in all_worksheets:
        worksheet = workbook.sheet_by_name(worksheet_name)
        print(file_to_import.replace(".xlsx",""))
        your_csv_file = open(''.join([path_to_import + file_to_import.replace(".xlsx",""), '.csv']), 'w',newline='')

        #print("CSV File Name - >>> ", your_csv_file.name)
        #print()

        wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

        #Loop through each row in the current worksheet
        for rownum in range(worksheet.nrows):
            csv_row = []
            for raw_entry in worksheet.row_values(rownum):
                #print("Cleaned up:  ", raw_entry," ",type(raw_entry))

                #make it a string and strip out embedded NL CR and Tabs
                tmp_str = str(raw_entry)
                tmp_str = tmp_str.replace('\n',' ').replace('\r',' ').replace('\t',' ')
                csv_row.append(tmp_str)
                #print ("Cleaned up:  ", tmp_str)
                #print ("CSV Row:  ", csv_row)

            #Loop thru all cells and find chars > 127
            output_row = []
            row_string = ''
#
            #loop over each cell in the row
            cellnum = 0

            for cell in csv_row:
                output_cell = ''
                cellnum = cellnum + 1
                #print(rownum,cellnum,cell)

                #loop over each char in the cell
                #look for any ascii character > 127
                #replace with a ? (question mark)
                for char in cell:
                    tmp = char
                    if ord(char) > 127:
                        #print("rownum: ",rownum, " found bad char: ",cell,tmp_str,char,ord(char))
                        tmp = chr(63)
                    output_cell = output_cell + tmp

                #If this Column cell contains a date convert it from an Excel Float to a date
                if rownum > 0 and cellnum == 5:
                    #print (rownum,cell)

                    #since this is a date turn it back to a float
                    cell = float(cell)

                    # 61 is the lowest Excel Date we can have due to leap year issues
                    if cell < 61:
                        cell = 61

                    #tmp_date = datetime.datetime(*xlrd.xldate_as_tuple(60., workbook.datemode))
                    tmp_date = datetime.datetime(*xlrd.xldate_as_tuple(cell, workbook.datemode))
                    #output_cell = tmp_date.strftime('%m/%d/%Y')
                    output_cell = tmp_date.strftime('%Y/%m/%d')
                    #print(workbook.datemode)

                row_string = row_string + output_cell
                output_row.append(output_cell)

            #Add the Hash Value for the row_string
            if rownum == 0:
                output_row.append('HashVal')
            else:
                output_row.append(hashlib.md5(row_string.encode('utf-8')).hexdigest())

            # Leave out the Header row
            if rownum != 0:
                wr.writerow([(str(entry)) for entry in output_row ])

    your_csv_file.close()
