# I'm going to use this to check if the flag is at half mast every day, and if it is, to alert me
import time
import ezgmail
import requests

if __name__ == '__main__':
    stars_and_stripes = requests.get('https://starsandstripesdaily.org/')
    print(stars_and_stripes.text)