from tkinter import *
from urllib.request import urlopen
from io import BytesIO
from numpy import pad
import requests, shutil
from PIL import ImageTk, Image
from bs4 import BeautifulSoup


def search(term):

    search_link = "https://www.mydramalist.com/search?q="+term+"&adv=titles&so=popular"

    page = requests.get(search_link)
    soup = BeautifulSoup(page.content, 'html.parser')

    searched_term = soup.find_all('a')[83]

    main_link = "https://www.mydramalist.com"+searched_term['href']

    return main_link


def get_info():
    page = requests.get(search(ent_search.get()))
    soup = BeautifulSoup(page.content, 'html.parser')
    drama_name = soup.find('h1').get_text()
    drama_nativetitle = soup.find_all('li', class_='list-item p-a-0')[12].get_text()
    drama_country = soup.find_all('li', class_='list-item p-a-0')[1].get_text()
    drama_episodes = soup.find_all('li', class_='list-item p-a-0')[2].get_text()
    drama_aired = soup.find_all('li', class_='list-item p-a-0')[3].get_text()
    drama_score = soup.find_all('li', class_='list-item p-a-0')[7].get_text()
    drama_genre = soup.find('li', class_='list-item p-a-0 show-genres').get_text()
    drama_synopsis = soup.find('p').get_text()

    l_cast, l_characters, l_role = [], [], []

    drama_cast_actors = soup.find_all('a', class_='text-primary text-ellipsis')
    for i in drama_cast_actors:
        l_cast.append(i.get_text())

    drama_characters = soup.find_all('div', class_='text-ellipsis')
    for j in drama_characters:    
        l_characters.append(j.get_text())

    drama_role = soup.find_all('small', class_='text-muted')
    for k in drama_role:
        l_role.append(k.get_text())

    s1 = ""
    s = f"{drama_name}\n{drama_nativetitle}\n{drama_country}\n{drama_episodes}\n{drama_aired}\n{drama_score}\n{drama_genre}\n\nSynopsis:\n{drama_synopsis}\n\nCast:\n"
    
    for l in l_cast:
        try:
            s1+=(f"{l} as {l_characters[l_cast.index(l)]} ({l_role[l_cast.index(l)]})\n")
        except:
            break

    drama_poster = soup.find('a', class_='block')['href']
    drama_poster_link = drama_poster.replace('/photos', 'https://i.mydramalist.com')+'c.jpg'
    print(drama_poster_link)

    r = requests.get(drama_poster_link, stream=True)
    if r.status_code == 200:
        with open("img.png", 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    
    return (s+s1, drama_name)

    
def show_info():


    txt_info = Text(frm_info, wrap=WORD, height=22, width=50)
    txt_info.grid(row=0, column=1, padx=10, pady=10)
    txt_info.insert('end', get_info()[0])
    txt_info.configure(state=DISABLED)
    img = ImageTk.PhotoImage(Image.open("img.png"))
    img_poster.configure(image=img)
    img_poster.image = img




def get_top20():
    btn_get_top20.configure(state=DISABLED)
    page = requests.get("https://mydramalist.com/shows/top_korean_dramas")
    soup = BeautifulSoup(page.content, 'html.parser')

    top_20 = soup.find_all('h6')
    bit_of_info = soup.find_all('span', class_='text-muted')

    top_20_window = Toplevel(root)
    top_20_window.title("Soju-Scraper V2 - Top 20 K-Dramas")
    top_20_window.resizable(0, 0)
    for i in range(10):
        Label(top_20_window, text=f"#{i+1} {top_20[i].get_text()} {bit_of_info[i].get_text()} \n", justify=LEFT).grid(row=i, column=0, padx=5, pady=5)
        Label(top_20_window, text=f"#{i+11} {top_20[i+10].get_text()} {bit_of_info[i+10].get_text()} \n", justify=LEFT).grid(row=i, column=1, padx=5, pady=5)
    btn_get_top20.configure(state=NORMAL)


def get_upcoming():
    page = requests.get("https://mydramalist.com/search?adv=titles&ty=68&co=3&st=2&so=date")
    soup = BeautifulSoup(page.content, 'html.parser')

    top_20 = soup.find_all('h6')
    bit_of_info = soup.find_all('span', class_='text-muted')

    top_20_window = Toplevel(root)
    top_20_window.title("Soju-Scraper V2 - Upcoming K-Dramas")
    top_20_window.resizable(0, 0)
    for i in range(10):
        Label(top_20_window, text=f"#{i+1} {top_20[i].get_text()} {bit_of_info[i].get_text()} \n", justify=LEFT).grid(row=i, column=0, padx=5, pady=5)
        Label(top_20_window, text=f"#{i+11} {top_20[i+10].get_text()} {bit_of_info[i+10].get_text()} \n", justify=LEFT).grid(row=i, column=1, padx=5, pady=5)

root = Tk()
root.title("Soju-Scraper V2")
root.resizable(0, 0)
    

frm_search = Frame(root)
frm_search.grid(row=0, column=0, padx=10, pady=10)
lbl_search = Label(frm_search, text="Search for KDrama:", font=(16))
lbl_search.grid(row=0, column=0, padx=10, pady=10)
ent_search = Entry(frm_search, width=20, font=('consolas', 12))
ent_search.grid(row=0, column=1, padx=10, pady=10)
btn_search = Button(frm_search, text="Search", command=lambda:show_info())
btn_search.grid(row=0, column=2, padx=10, pady=10)

frm_other = Frame(root)
frm_other.grid(row=1, column=0, padx=10, pady=10)
btn_get_top20 = Button(frm_other, text='Top 20 K-Dramas', command=lambda:get_top20())
btn_get_top20.grid(row=0, column=0, padx=5)
btn_get_upcoming = Button(frm_other, text='Upcoming K-Dramas', command=lambda:get_upcoming())
btn_get_upcoming.grid(row=0, column=1, padx=5)

root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='icon.png'))

frm_info = Frame(root, height=400, width=650)
frm_info.grid(row=2, column=0, padx=10, pady=10)
img_poster = Label(frm_info)
img_poster.grid(row=0, column=0, padx=10, pady=10)



root.mainloop()
