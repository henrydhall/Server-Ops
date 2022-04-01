# I'm going to use this to check if the flag is at half mast every day, and if it is, to alert me

# Dependencies this program uses.
import ezgmail
import requests
import os
from pathlib import Path

def get_addresses():
    """
    # returns: list of strings.
    # Used to get the addresses. Read line by line from addresses.txt
    # The user will need to add addresses to the file themselves.
    """
    try:
        address_file = Path('addresses.txt')
        addresses = address_file.read_text()
        addresses = addresses.splitlines()
    except:
        raise ValueError('***It seems there is not an addresses file. Please add it!***')
    if len(addresses) < 1:
        raise ValueError('No addresses.')
    return addresses

def send_status_email(text_to_send):
    # You'll need to change this to whatever the correct directory is.
    try:
        os.chdir(r'/home/henry/Git Folders/Server-Ops-Git/Half-Mast-Checker/')
    except:
        raise SystemError('Directory not found.')
    try:
        ezgmail.init()
    except:
        raise SystemError('Problem with token, check other errors.')
    
    addresses = get_addresses()

    # Send to each receiver one by one.
    for receiver in addresses:
        ezgmail.send(receiver, 'Today\'s Flag Status', text_to_send)

def get_national_status():
    """
    # Returns strings 'FULL STAFF' or 'HALF STAFF' depending on stars and stripes daily.
    """
    stars_and_stripes_text = get_stars_and_stripes()
    national_flag_status = get_stars_and_stripes_status(stars_and_stripes_text)
    return national_flag_status

def get_stars_and_stripes():
    # Get the page from SSD make it text.
    stars_and_stripes_page = requests.get('https://starsandstripesdaily.org/') # Use this to get the SSD page
    stars_and_stripes_text = stars_and_stripes_page.text # Get the page as text.
    return stars_and_stripes_text

def get_stars_and_stripes_status(page_as_text):
    """
    # Parameters: 
    #   page_as_text: the stars and stripes website page as text.
    # Returns:
    #   flag_status: 'HALF STAFF' or 'FULL STAFF' depending on ssd
    """

    # Initialize the flag status as none.
    flag_status = 'none'

    # Process text, get the status line.
    my_text = page_as_text.split('\n')
    for i in range(0,len(my_text)):
        my_text[i] = my_text[i].strip()
    if '<h3>The status of the American Flag today is</h3>' in my_text:
        flag_status = get_starsandstripes_status_line(my_text)
    else:
        flag_status = 'unable to get status'

    # If 'FULL STAFF' is in the status line, set the status to full staff
    if 'FULL STAFF' in flag_status:
        flag_status = 'FULL STAFF'
    elif 'HALF STAFF' in flag_status: # If it's half staff, set to half staff
        flag_status = 'HALF STAFF'

    return flag_status

def get_starsandstripes_status_line(text_to_search):
    # Finds the status line based on the line that should be right before it.
    previous_line = '<h3>The status of the American Flag today is</h3>'
    line_number = text_to_search.index(previous_line)
    status_line = line_number + 1
    flag_status = text_to_search[status_line]
    return flag_status

def get_utah_status():
    utah_stat = 'none'
    utah_stat = requests.get('https://governor.utah.gov/flag-status/') # Use this to get the Utah flat status page
    utah_text = utah_stat.text
    for line in utah_text.split('\n'):
        if 'The flag of the United States of America and the flag of the state of Utah are currently at' \
            in line:
            if 'full-staff' in line:
                utah_stat = 'FULL STAFF'
            elif 'half-staff' in line:
                utah_stat = 'HALF STAFF'
    return utah_stat

def email_flag_status(send_email = True):
    """
    # Using this to clean up the code. Does everything to compile and send the email.
    """
    # Initialize email message
    email_report = ''
    # Set a default status.
    national_flag_status = 'none'
    utah_stat = 'none'

    # Get the statuses
    national_flag_status = get_national_status()
    utah_stat = get_utah_status()

    # Assemble email message.
    email_report = email_report + 'Today\'s Flag Status: \n' + f'National Status: {national_flag_status}' \
        + '\n' + f'Utah Status: {utah_stat}' + '\n' \
            + 'For more info see https://starsandstripesdaily.org/ and https://governor.utah.gov/flag-status/'
    if send_email == True:
        send_status_email(email_report)
    else:
        return email_report

if __name__ == '__main__':
    email_flag_status(True)
