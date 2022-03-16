# I'm going to use this to check if the flag is at half mast every day, and if it is, to alert me
import time
import ezgmail
import requests
from pathlib import Path

def get_status(text_to_search):
    previous_line = '<h3>The status of the American Flag today is</h3>'
    line_number = text_to_search.index(previous_line)
    status_line = line_number + 1
    flag_status = text_to_search[status_line]
    return flag_status

if __name__ == '__main__':
    # Set a default status.
    flag_status = 'none'

    # Get the page from SSD make it text.
    stars_and_stripes = requests.get('https://starsandstripesdaily.org/') # Use this to get the SSD page
    my_text = stars_and_stripes.text
    
    # Process text, get what I believe is the status line.
    my_text = my_text.split('\n')
    for i in range(0,len(my_text)):
        my_text[i] = my_text[i].strip()
    if '<h3>The status of the American Flag today is</h3>' in my_text:
        flag_status = get_status(my_text)
    else:
        flag_status = 'unable to get status'
    # Print status line to test.
    print(flag_status)

    # If 'FULL STAFF' is in the status line, set the status to full staff
    if 'FULL STAFF' in flag_status:
        flag_status = 'FULL STAFF'
    
    # Send status.
    # TODO: Send status.
    # TODO: Run regularly.