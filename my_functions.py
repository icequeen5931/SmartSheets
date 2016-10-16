__author__ = 'jpisano'
import xlrd
import csv
import hashlib

# a change

def csv_from_excel(path_to_import,file_to_import):
    #This function reads an excel sheet and creates a CSV file
    excel_file = path_to_import + file_to_import
    workbook = xlrd.open_workbook(excel_file)
    all_worksheets = workbook.sheet_names()
    print ("Sheets - >>>>  ",all_worksheets)
    print()

    #Loop through all the worksheets
    for worksheet_name in all_worksheets:
        worksheet = workbook.sheet_by_name(worksheet_name)

        your_csv_file = open(''.join([path_to_import + worksheet_name, '.csv']), 'w',newline='')

        print("CSV File Name - >>> ", your_csv_file.name)
        print()

        wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

        #Loop through each row in the current worksheet
        for rownum in range(worksheet.nrows):
            csv_row = []
            for raw_entry in worksheet.row_values(rownum):

                #make it a string and strip out NL CR and Tabs
                tmp_str = str(raw_entry)
                tmp_str = tmp_str.replace('\n',' ').replace('\r',' ').replace('\t',' ')
                csv_row.append(tmp_str)
                #print ("Cleaned up:  ", tmp_str)
                #print ("CSV Row:  ", csv_row)

            #Loop thru all cells and find chars > 127
            output_row = []
            jim = ''
#
            #loop over each cell in the row
            for cell in csv_row:
                output_cell = ''
                output_char = ''

                #loop over each char in the cell
                for char in cell:
                    tmp = char
                    if ord(char) > 127:
                        tmp = chr(63)

                    output_cell = output_cell + tmp

                jim = jim + output_cell

                output_row.append(output_cell)


            #print ("Output Row: ",output_row)
            if rownum == 0:
                output_row.append('HashVal')
            else:
                output_row.append(hashlib.md5(jim.encode('utf-8')).hexdigest())

            #print('md5 hash - >>> ', hashlib.md5(jim.encode('utf-8')).hexdigest())
            #print(jim)
            #print()
            wr.writerow([(str(entry)) for entry in output_row ])

    your_csv_file.close()
