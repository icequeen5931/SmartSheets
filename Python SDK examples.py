__author__ = 'jpisano'

import smartsheet
my_token = '1whrobtxnyffk49x4ldrtrljk0'
smartsheet = smartsheet.Smartsheet(my_token)


#This work
me = smartsheet.Users.get_current_user()
aa = me.to_dict()
print(aa)

print()
print('user:   ',aa['lastName'])
print()


dnld_dir='c:/users/jpisano/desktop/ACI to Production Database/Todays Data/'
cust_name='2K GAMES INC'

action = smartsheet.Sheets.list_sheets(include_all=True)
sheets = action.data #Returns a list of smartsheet SHEET objects

#Loop through all sheets
for sheetInfo in sheets:

    # Here is the Sheet we are looking for
    #if sheetInfo.name == 'ACI to Production 11-30-15 Commercial':
    if sheetInfo.name == 'cust_ref_ps':
        #my_sheet = smartsheet.Sheets.get_sheet(sheet.id,include='rowNumbers')
        #my_sheet = smartsheet.Sheets.get_sheet(sheetInfo.id,include=['format'],row_numbers=['20,23,657'])
        my_sheet = smartsheet.Sheets.get_sheet(sheetInfo.id,page_size=500)

        print(sheetInfo.name,'  ',action.total_count ,'  ',action.total_pages)
        print (my_sheet.total_row_count)

        #Gather the row and column objects
        col_objs = my_sheet.columns
        row_objs = my_sheet.rows

        for my_col in col_objs:
            if my_col.title == 'End Customer Global Ultimate Name':
                col_id = my_col.id

            if my_col.title == 'Assigned PSS':
                pss_col_id = my_col.id

        for my_row in row_objs:

            if my_row.get_column(col_id).value == cust_name:
                my_cells = my_row.cells
                for my_cell in my_cells:
                    print (my_cell.value,' /  ',end='')

                new_pss_cell = my_row.get_column(pss_col_id)
                new_pss_cell.value = 'stan'
                my_row.set_column(new_pss_cell.column_id, new_pss_cell)

                smartsheet.Sheets.update_rows(sheetInfo.id, [my_row])

# print(ang.name)


#
# # This works !
# # smartsheet.Sheets.get_sheet_as_csv(sheet_id,dnld_dir)
# # smartsheet.Sheets.get_sheet_as_excel(sheet_id,dnld_dir)
#
#
# action = smartsheet.Sheets.get_columns(sheet_id, include_all=True)
# columns = action.data
#
# # Get paginated list of columns (100 columns per page).
# # action = smartsheet.Sheets.get_columns(sheet_id)
# # pages = action.total_pages
# # columns = action.data
#
# #This works !
# row = smartsheet.Sheets.get_row(
#     sheet_id,row_id)
#     #include='columns')
# #     #include='discussions,attachments,columns,columnType')
#
# column = smartsheet.Sheets.get_column(sheet_id, col_id,)
# for item in column:
#     print (column[item])
#
# #cell = row.get_column(sheet_id,col_id)
# #print(row.get_column('4113607471458180'))
# #print (cell)
# #print (row)
# print ('Type: ', type(sheets),type(row),type(columns),type(action))
# print()
# #print (action)
#
# print()
# #print (columns)
# print (type(columns))
# print()
# for c in columns:
#     #print(c["End Customer Global Ultimate Name"])
#     print (type(c))
#     #print([]
#     break
#
#
#
# #type(cell.value)
# #print (cell.value)
#
# #print (row.get('sheetId'))
# # for cell in row:
# #     print (cell)
#
# #print (row)
#
#
#
# # sh = sheets.data
# #
# #for i in sh:
# #    print(i)
#
# #print (smartsheet.version)

