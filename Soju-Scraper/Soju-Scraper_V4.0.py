from tkinter import *
from urllib.request import urlopen
import requests, shutil
from PIL import ImageTk, Image
from bs4 import BeautifulSoup
from tkscrolledframe import ScrolledFrame
import threading



def get_info(drama):
    search_link = "https://www.mydramalist.com/search?q="+drama+"&adv=titles&co=3&so=popular"

    page = requests.get(search_link)
    soup = BeautifulSoup(page.content, 'html.parser')

    searched_term = soup.find_all('a')[83]

    main_link = "https://www.mydramalist.com"+searched_term['href']

    page = requests.get(main_link)
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
    drama_characters = soup.find_all('div', class_='text-ellipsis')
    drama_role = soup.find_all('small', class_='text-muted')
    s1 = ""
    for (i, j, k) in zip(drama_cast_actors, drama_characters, drama_role):
        l_cast.append(i.get_text())
        l_characters.append(j.get_text())
        l_role.append(k.get_text())
        s1+=(f"{i.get_text()} as {j.get_text()} ({k.get_text()})\n")


    s = f"{drama_name}\n{drama_nativetitle}\n{drama_country}\n{drama_episodes}\n{drama_aired}\n{drama_score}\n{drama_genre}\n\nSynopsis:\n{drama_synopsis}\n\nCast:\n"
    

    drama_poster = soup.find('a', class_='block')['href']
    drama_poster_link = drama_poster.replace('/photos', 'https://i.mydramalist.com')+'c.jpg'
    print(drama_poster_link)

    r = requests.get(drama_poster_link, stream=True)
    if r.status_code == 200:
        with open("img.png", 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    
    

    txt_info = Text(frm_info, wrap=WORD, height=22, width=50)
    txt_info.grid(row=0, column=1, padx=10, pady=10)
    txt_info.insert('end', s+s1)
    txt_info.configure(state=DISABLED)
    
    img = ImageTk.PhotoImage(Image.open("img.png"))
    img_poster.configure(image=img)
    img_poster.image = img


def get_list(link, title):
    titles = []
    for pg in range(1,6):
        page = requests.get(f"{link}&page={pg}")
        soup = BeautifulSoup(page.content, 'html.parser')

        top_20 = soup.find_all('h6')
        bit_of_info = soup.find_all('span', class_='text-muted')

        for i in top_20:
            a = i.get_text()+bit_of_info[top_20.index(i)].get_text()
            titles.append(a)

    root1 = Toplevel()
    root1.title(title)
    root1.resizable(0, 0)
    sf = ScrolledFrame(root1, width=590, height=650)
    sf.grid(row=0, column=0)

    sf.bind_arrow_keys(root1)
    sf.bind_scroll_wheel(root1)

    inner_frame = sf.display_widget(Frame)

    for j in range(0, len(titles), 2):
        Label(inner_frame, text=f"#{j+1} {titles[j]}", justify=LEFT, width=35, borderwidth=1, relief="solid").grid(row=j, column=0, padx=5, pady=5)
        Label(inner_frame, text=f"#{j+2} {titles[j+1]}", justify=LEFT, width=35, borderwidth=1, relief="solid").grid(row=j, column=1, padx=5, pady=5)

        

def get_top20():
    btn_get_top20.configure(state=DISABLED)
    link = "https://mydramalist.com/shows/top_korean_dramas/?"
    title = "Soju-Scraper V4 - Top K-Dramas"
    get_list(link, title)
    btn_get_top20.configure(state=NORMAL)


def get_upcoming():
    btn_get_upcoming.configure(state=DISABLED)
    link = "https://mydramalist.com/search?adv=titles&ty=68&co=3&st=2&so=date"
    title = "Soju-Scraper V4 - Upcoming K-Dramas"
    try:    
        get_list(link, title)
    except IndexError:
        pass
    btn_get_upcoming.configure(state=NORMAL)



def get_newest():
    btn_get_newest.configure(state=DISABLED)
    link = "https://mydramalist.com/search?adv=titles&ty=68&co=3&so=newest&or=asc"
    title = "Soju-Scraper V4 - Latest K-Dramas"
    get_list(link, title)
    btn_get_newest.configure(state=NORMAL)


def about():
    info = """Version: 4.0
\nDependencies:\n   - requests\n   - BeautifulSoup4\n   - tkscrolledframe

All data in this application are webscraped from https://www.mydramalist.com/\n
 Found issues? Reach me at @__bitan005__ on Instagram\n\nMade with Love by Bitan"""
    about_window = Toplevel(root)
    about_window.title("Soju-Scraper V3 - About")
    about_window.resizable(0, 0)
    Label(about_window, font=('', 32, 'bold underline'), text="Soju-Scraper").pack(padx=10, pady=10)
    Label(about_window, text=info, justify=LEFT, font=('', 12)).pack(ipadx=20, ipady=20)

    

root = Tk()
root.title("Soju-Scraper V4")
root.resizable(0, 0)
    

frm_search = Frame(root)
frm_search.grid(row=0, column=0, padx=10, pady=10)
lbl_search = Label(frm_search, text="Search for KDrama:", font=(16))
lbl_search.grid(row=0, column=0, padx=10, pady=10)
ent_search = Entry(frm_search, width=20, font=('consolas', 12))
ent_search.grid(row=0, column=1, padx=10, pady=10)
btn_search = Button(frm_search, text="Search", command=lambda:threading.Thread(target=get_info(ent_search.get())).start())
btn_search.grid(row=0, column=2, padx=10, pady=10)


frm_other = Frame(root)
frm_other.grid(row=1, column=0, padx=10, pady=10)
btn_get_top20 = Button(frm_other, text='Top K-Dramas', command=lambda:threading.Thread(target=get_top20).start())
btn_get_top20.grid(row=0, column=0, padx=5)
btn_get_newest = Button(frm_other, text='Latest K-Dramas', command=lambda:threading.Thread(target=get_newest).start())
btn_get_newest.grid(row=0, column=1, padx=5)
btn_get_upcoming = Button(frm_other, text='Upcoming K-Dramas', command=lambda:threading.Thread(target=get_upcoming).start())
btn_get_upcoming.grid(row=0, column=2, padx=5)
btn_about = Button(frm_other, text='About', command=about)
btn_about.grid(row=0, column=3, padx=5)

root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='icon.png'))

frm_info = Frame(root, height=400, width=650)
frm_info.grid(row=2, column=0, padx=10, pady=10)
img_poster = Label(frm_info)
img_poster.grid(row=0, column=0, padx=10, pady=10)



root.mainloop()
