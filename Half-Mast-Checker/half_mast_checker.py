# I'm going to use this to check if the flag is at half mast every day, and if it is, to alert me
import time
import ezgmail
import requests
from pathlib import Path

def get_stars_and_stripes():
    # Get the page from SSD make it text.
    stars_and_stripes = requests.get('https://starsandstripesdaily.org/') # Use this to get the SSD page
    my_text = stars_and_stripes.text
    return my_text

def get_stars_and_stripes_status(string_to_check):
    flag_status = 'none'

    # Process text, get what I believe is the status line.
    my_text = string_to_check.split('\n')
    for i in range(0,len(my_text)):
        my_text[i] = my_text[i].strip()
    if '<h3>The status of the American Flag today is</h3>' in my_text:
        flag_status = get_status_line(my_text)
    else:
        flag_status = 'unable to get status'

    # If 'FULL STAFF' is in the status line, set the status to full staff
    if 'FULL STAFF' in flag_status:
        flag_status = 'FULL STAFF'
    elif 'HALF STAFF' in flag_status: # If it's half staff, set to half staff
        flag_status = 'HALF STAFF'

    return flag_status

def get_status_line(text_to_search):
    previous_line = '<h3>The status of the American Flag today is</h3>'
    line_number = text_to_search.index(previous_line)
    status_line = line_number + 1
    flag_status = text_to_search[status_line]
    return flag_status

def get_utah_status():
    utah_stat = 'none'
    utah_stat = requests.get('https://governor.utah.gov/flag-status/') # Use this to get the SSD page
    utah_text = utah_stat.text
    for line in utah_text.split('\n'):
        if 'The flag of the United States of America and the flag of the state of Utah are currently at' \
            in line:
            if 'full-staff' in line:
                utah_stat = 'FULL STAFF'
            elif 'half-staff' in line:
                utah_stat = 'HALF STAFF'
    return utah_stat

if __name__ == '__main__':
    # Set a default status.
    national_flag_status = 'none'
    my_text = get_stars_and_stripes()
    national_flag_status = get_stars_and_stripes_status(my_text)

    utah_stat = get_utah_status()

    print(f'National Status: {national_flag_status}')
    print(f'Utah Status: {utah_stat}')
    
    ezgmail.init()

    # Send status.
    # TODO: Send status.
    # TODO: Run regularly.