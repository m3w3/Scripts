import urllib.request
import requests
################################################################################
# Get the relevant info from user

validate1 = 'n'
while validate1 != 'y':
    current_year = '0'
    # sanity check for year entered
    while len(current_year) != 4:
        current_year = input('\nEnter the year of the breakdown: ')

    form_type = ''
    while form_type not in ['T3', 'T5', 'T5013']:
        form_type = input('T3, T5, or T5013: ')

    validate1 = input("\nYou've entered: " + form_type + \
                     " for year " + current_year + ". Is this correct? (y/n)")

print("\nCreate a list of all the " + form_type + " CUSIPs that were actually used."  + '\n' \
      + "Put the list in a .txt file with no headers; cusip values should be 9-digit."  + '\n' \
      + "Note that the .txt file should only contain 1 column (list of all used CUSIPs).")

validate2 = 'n'
while validate2 != 'y':
    used_cusip = input("Specify the location and filename of the .txt file here."  + '\n' \
                       + r"***i.e. C:\Users\ziyue.wu\Desktop\Used_" + form_type + "_CUSIPs.txt***" + '\n')

    save_location = input('\n' + r'Specify a save location. For example, C:\Desktop\ ' + '\n' \
                          + r'Remember to include backslash \ at the very end!' + '\n')

    validate2 = input("\nUsed-CUSIP list file location entered: " + used_cusip + "\n" \
                      + "Download folder save location entered: " + save_location + "\n" \
                      + "Is this correct? (y/n)")

used_cusips = open(used_cusip).read()

print('\nInitializing, this could take several minutes...' + '\n' \
      + '***Press CTRL + C (copy input) if you wish to stop at any time.***' + '\n')
##########################################################################################
# Set up the initializing process

cds_web = requests.get('https://services.cds.ca/applications/taxforms/taxforms.nsf/' \
                           + 'processed-EN-?OpenView&Start=1&Count=3000&RestrictToCategory=' \
                           + form_type + '-' + current_year)

page_text = cds_web.text[cds_web.text.index('><SPAN CLASS="Date" >'):cds_web.text.index\
                           ('var st2 = new SortableTable(document.getElementById("taxlist")')]

# Use a loop and obtain all CUSIP file addresses
# Note the file names are always 92-character length, for example:
# './0/8CC143800F9CDC038525802D007E4780/$File/CDSP-ADRUY4_T3_R16_TY2016_2016_09_13_18_59_18.xls'

#Place all the references in a dictionary
qc_equiv = {'T3': 'R16', 'T5': 'R3', 'T5013': 'R15'}
cusip_links = {}
cusip_dates = {}
cusip_types = {}

#All trackers/reference tools:
date_track = 0
cusip_track = 0
revise_track = 0
type_track = 0
link_beg_track = 0
link_end_track = 0
processing = 0
##########################################################################################
#Sort data into listed variables

# note that "page_text.count('./0/') + 1" is the total CUSIP count on the webpage
for x in range(1, page_text.count('./0/') + 1):

    # Track location of next <SPAN CLASS="Cusip" >
    cusip_track = page_text.find('<SPAN CLASS="Cusip" >', cusip_track + 21)

    # Track location of next <SPAN CLASS="Date" >
    date_track = page_text.find('<SPAN CLASS="Date" >', date_track + 1)

    # Track location of next <SPAN CLASS="Type" >
    type_track = page_text.find('<SPAN CLASS="Type" >', type_track + 20)

    # Track location of next ./0/
    link_beg_track = page_text.find('./0/', link_beg_track + 91)

    # Track location of next .xls
    link_end_track = page_text.find('.xls', link_end_track + 91)

    # Check if the CUSIP is empty
    if page_text[cusip_track + 21:cusip_track + 30].find("/") >= 0:
        cusip = 'EMPTY ERROR!'
    else:
        cusip = page_text[cusip_track + 21:cusip_track + 30]

    # Only store the data if they're used in our dividend transactions
    if cusip in used_cusips:
        # i.e. 11/28/2017 12:10:06 -> 11282017121006
        date_CUSIP1 = page_text[date_track + 20:date_track + 39].\
                      replace('/', '').replace(':', '').replace(' ', '')
        # i.e. 11282017121006 -> 20171128121006
        date_CUSIP2 = date_CUSIP1[4:8] + date_CUSIP1[0:4] + date_CUSIP1[8:14]

        # slips with RL-breakdowns will use "," as deliminators
        # i.e. T5013, R15
        raw_type = page_text[type_track + 20:type_track + 30]

        # check for cases where RL-breakdowns exist
        type_cusip = form_type
        if raw_type.find(',') != -1:
            type_cusip += ", " + qc_equiv[form_type]

        # Put the dates, types, and links into their respective CUSIPs
        # page_text is in earliest-to-latest-sorting
        # Only keep the CUSIPs with latest dates
        # Replace existing CUSIP if new CUSIP data shows up
        cusip_dates[cusip] = int(date_CUSIP2)
        cusip_types[cusip] = type_cusip
        cusip_links[cusip]='https://services.cds.ca/applications/taxforms/taxforms.nsf'\
                            + page_text[link_beg_track + 1:link_end_track + 4]

# total cusips to download
found_cusips = str(len(cusip_links))
##########################################################################################
# Grab the files

for _cusip in cusip_links:
    processing += 1
    print("Processing " + str(processing) + " of " + found_cusips + " CUSIP.")
    
    urllib.request.urlretrieve(cusip_links[_cusip], save_location + \
                               _cusip + '_' + str(cusip_dates[_cusip]) \
                               + '_' + cusip_types[_cusip] + '.xls')

print('\nFinished downloading ' + found_cusips + ' total ' + form_type + ' breakdowns from CDS.' + \
      '\nGo to **' + save_location[:-1] + '** to see your files.')
