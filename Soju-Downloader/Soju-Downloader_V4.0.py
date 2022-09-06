from urllib.request import urlopen
from io import BytesIO
import requests, shutil
from bs4 import BeautifulSoup
import os

term = input("Enter drama to search:")

search_link = "https://www.mydramalist.com/search?q="+term+"&adv=titles&so=popular"

page = requests.get(search_link)
soup = BeautifulSoup(page.content, 'html.parser')

searched_term = soup.find_all('a')[83]

main_link = "https://www.mydramalist.com"+searched_term['href']

pg = 1
pages = []

print("\n", searched_term.get_text(), "\n\nGetting Info... Please wait.")
for pg in range(1,21):
    try_page_link = main_link+f"/photos?page={pg}"
    pages.append(try_page_link)


page = requests.get(main_link)
soup = BeautifulSoup(page.content, 'html.parser')

drama_name = soup.find('h1').get_text()
print("\n\n", drama_name)
  
downloaded = []
set_downloaded = False
print("\nGetting download links...")
for current_page in pages:
    page = requests.get(current_page)
    soup = BeautifulSoup(page.content, 'html.parser')

    drama_images = soup.find_all('a', class_='block')
    if set_downloaded==False:
        for drama_image in drama_images:
            drama_image_link = drama_image['href'].replace('/photos', 'https://i.mydramalist.com')+'.jpg'
            if drama_image_link in downloaded:
                break
                set_downloaded = True
            else:
                downloaded.append(drama_image_link)
    else:
        break
    
        
        

i = 0

conf = input(f"There are total {len(downloaded)} files. Do you want to continue?[y/n]").lower()
if conf=="y":

    if os.path.exists(drama_name):
        print("Folder exists... Download Cancelled.")
    else: 
        os.mkdir(drama_name)
        print("\nStarting Download...\n")
        print("Directory created")  
        for j in downloaded:
            i+=1
            percentage = i/len(downloaded)
            r = requests.get(j, stream=True)
            if r.status_code == 200:        
                print(f"[{i} of {len(downloaded)}] Downloading: ", j, round(percentage*100, 2), '%')
                with open(f"{drama_name}/{drama_name} {i}.jpg", 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)

        print("\n\nAll photos downloaded successfully.")

else:
    pass


