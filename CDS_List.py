import requests
import datetime
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

show_qc = input("\nIndicate whether the CUSIP is Quebec? (y/n)")
print("\nProcessing...\n")
################################################################################
# Set up the initializing process

cds_web = requests.get('https://services.cds.ca/applications/taxforms/taxforms.nsf/' \
                           + 'processed-EN-?OpenView&Start=1&Count=3000&RestrictToCategory=' \
                           + form_type + '-' + current_year)

page_text = cds_web.text[cds_web.text.index('><SPAN CLASS="Date" >'):cds_web.text.index\
                           ('var st2 = new SortableTable(document.getElementById("taxlist")')]

# Setup all type references
if show_qc == 'y':
    qc_equiv = {'T3': 'R16', 'T5': 'R3', 'T5013': 'R15'}
    cusip_types = {}
    type_track = 0
else:
    cusip_list = []

# Loop tracker:
cusip_track = 0
##########################################################################################
#Sort data into listed variables

# note that "page_text.count('./0/') + 1" is the total CUSIP count on the webpage
for x in range(1, page_text.count('./0/') + 1):

    # Track location of next <SPAN CLASS="Cusip" >
    cusip_track = page_text.find('<SPAN CLASS="Cusip" >', cusip_track + 21)

    # Check if the CUSIP is not empty
    if page_text[cusip_track + 21:cusip_track + 30].find("/") < 0:
        cusip = page_text[cusip_track + 21:cusip_track + 30]

    if show_qc == 'y':
        
        # Track location of next <SPAN CLASS="Type" >
        type_track = page_text.find('<SPAN CLASS="Type" >', type_track + 20)

        # slips with RL-breakdowns will use "," as deliminators
        # i.e. T5013, R15
        raw_type = page_text[type_track + 20:type_track + 30]

        # check for cases where RL-breakdowns exist
        if raw_type.find(',') == -1:
            type_cusip = form_type
        else:
            type_cusip = qc_equiv[form_type]

        # Put the type into its CUSIP dictionary
        # page_text is in earliest-to-latest-sorting
        # Only keep the CUSIPs with latest dates
        # Replace existing CUSIP if new CUSIP data shows up
        cusip_types[cusip] = type_cusip

    else:
        cusip_list.append(cusip)
##########################################################################################
# Print the list of CUSIPs

# total non-empty cusips on webpage
if show_qc == 'y':
    _total = str(len(cusip_types))
    for cusips_ in cusip_types:
        print(cusips_ + ", " + cusip_types[cusips_])
else:
    # convert list to set then back to list (to remove dupes)
    cusip_list = list(set(cusip_list))
    _total = str(len(cusip_list))
    for cusips_ in cusip_list:
        print(cusips_)

# Import current datetime and format it
_datetime1 = datetime.datetime.now().__str__()
_datetime2 = _datetime1[0: _datetime1.index(".")]

print("\nTotal of " + _total + " " + form_type + " breakdowns in " \
      + current_year + ", as of " + _datetime2 + ".")
