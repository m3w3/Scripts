# Scripts
CDS_Download.py:
Downloads everything from:
https://services.cds.ca/applications/taxforms/taxforms.nsf/PROCESSED-EN-?OpenView&Start=1&Count=3000&RestrictToCategory=All-2019. In addition, only the LATEST breakdown file will be downloaded, and the Excel files will be renamed properly.

CDS_List.py:
Lists every CUSIP (in 9-digit value) from the CDS website, given the year and tax form type (i.e. all CUSIPs available for T3 in year 2018).

Excel_to_CSV.py:
Creates a new CSV file from an existing Excel file using dataframe.
