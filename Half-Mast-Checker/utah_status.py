import requests

utah_stat = requests.get('https://governor.utah.gov/flag-status/') # Use this to get the SSD page
utah_text = utah_stat.text

#print(utah_text)

for line in utah_text.split('\n'):
    if 'The flag of the United States of America and the flag of the state of Utah are currently at' \
        in line:
        print(line)
        if 'full-staff' in line:
            print('FULL STAFF')