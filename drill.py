# Import required modules
import requests
from bs4 import BeautifulSoup
import unidecode
import pandas as pd
import re
import os

base_url = 'https://www.churchofjesuschrist.org'
all_conference_url = '/study/general-conference?lang=eng'
download_path = 'downloads'

def get_conference(url):
  request = requests.get(base_url+url)
  conf = BeautifulSoup(request.content.decode('utf-8'), features="lxml")
  for ref in conf('a', href=True):
    x = re.findall('[0-9]+[a-z]+', ref['href'])
    if len(x) > 0:
      if len(ref.contents[0]) > 1:
        name_full = ref.contents[0].contents[1].get_text()
        nums = re.findall(r'\d+', ref['href'])
        name = unidecode.unidecode(name_full).lower().replace(' ','-').replace('.','')
        year = nums[0]
        mon = nums[1]
        digit1 = nums[2][0]
        digit2 = nums[2][1]
        monName = 'april' if mon == '04' else 'october'

        if len(name_full) > 3:
          download_url = f'https://media2.ldscdn.org/assets/general-conference/{monName}-{year}-general-conference/{year}-{mon}-{digit1}0{digit2}0-{name}-32k-eng.mp3?lang=eng&download=true'
          print(download_url)
          download_file(download_url, f'{year}-{monName}-{digit1}0{digit2}0-{name}.mp3')


def download_file(url, filename):
  if not os.path.exists(download_path):
    os.makedirs(download_path)
  r = requests.get(url, allow_redirects=True)
  open(os.path.join(download_path,filename), 'wb').write(r.content)


# Scrape the HTML at the url
r = requests.get(base_url+all_conference_url)

# Turn the HTML into a Beautiful Soup object
soup = BeautifulSoup(r.text, features="lxml")

for ref in soup('a', href=True):
  if '2023' in ref['href']:
    get_conference(ref['href'])

# for elem in soup(text=re.compile(r'2022')):
#   print(elem.parent.parent)



#"https://media2.ldscdn.org/assets/general-conference/april-2022-general-conference/2022-04-5070-dieter-f-uchtdorf-32k-eng.mp3?lang=eng&download=true"

#"https://assets.ldscdn.org/4f/26/4f262b70b2bc11ecbc74eeeeac1e7455acbacd5a/2022_04_come_we_that_love_the_lord_eng.mp3?lang=eng&download=true"
#https://assets.ldscdn.org/72/a1/72a11dd5b2bc11ec97a0eeeeac1ef4e21947761c/2022_04_rejoice_the_lord_is_king_eng.mp3?lang=eng&download=true"