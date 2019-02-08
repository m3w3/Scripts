import pandas as pd
import math
import csv

"""THIS SCRIPT IS LIBRARY DEPENDENT!
Start -> Run -> type "cmd" (without the quotes)
Type: "pip install pandas xlrd xlwt" (without the quotes)
Wait for download to finish, then exit cmd."""

validate1 = 'n'
while validate1 != 'y':
    excel_file = input("Specify the location and filename of the EXCEL file."  + '\n'
                       + r"***i.e. D:/test.xlsx***" + '\n')

    validate1 = input("\nYou've entered: " + excel_file
                      + " Is this correct? (y/n)")

excel_len = len(excel_file)
path_d = excel_len - 1 - excel_file[::-1].find('/')

validate2 = 'n'
while validate2 != 'y':
    sheet_str = input("Specify the sheet number of your workbook (i.e. 1, 2, ...).\n")

    validate2 = input("\nYou've entered: " + sheet_str + " Is this correct? (y/n)")

# sheet name or sheet number or list of sheet numbers and names
sheet = int(sheet_str) - 1

df = pd.read_excel(excel_file, sheet_name=sheet, na_values="") # read excel file

header = list(df)
hash_ = {}
i = 1
for index, row in df.iterrows(): # iterate over each row
    hash_[i] = []
    hash_index = hash_[i]
    
    for column in header:
        cell_val = row[column]
        
        if isinstance(cell_val, int) or isinstance(cell_val, float):
            if math.isnan(cell_val):
                hash_index.append("")
            else:
                hash_index.append(round(cell_val, 2))
        else:
            hash_index.append(str(cell_val))
    i += 1

# TEST HASH MAP
##for key in hash_:
##    print (key, hash_[key])

with open(excel_file[:-5] + '.csv', 'w', newline='') as csvfile:
    csvfile.truncate()
    writer = csv.writer(csvfile, delimiter=',')
    
    writer.writerow(header)
    for row_index in range(1, i): # could also use len(df.index) instead of i
        writer.writerow(hash_[row_index])

print("\nFinished! CSV file '{}' located at '{}'.\n".format(
    excel_file[path_d + 1:excel_len - 5] + '.csv', excel_file[:path_d]))
print("Check the CSV file using Notepad (Right Click -> Edit)")
