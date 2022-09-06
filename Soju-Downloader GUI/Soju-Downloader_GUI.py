from tkinter import *
from urllib.request import urlopen
import requests, shutil, os, threading
from bs4 import BeautifulSoup
from tkinter import messagebox


def start_download():
    btn_search.configure(state=DISABLED)
    txt_status.delete(0.0, END)
    term = ent_search.get()
    search_link = "https://www.mydramalist.com/search?q="+term+"&adv=titles&so=popular"

    page = requests.get(search_link)
    soup = BeautifulSoup(page.content, 'html.parser')

    searched_term = soup.find_all('a')[83]

    main_link = "https://www.mydramalist.com"+searched_term['href']

    pg = 1
    pages = []

    txt_status.insert(END, f"You searched for {searched_term.get_text()} \nGetting Info... Please wait.")
    for pg in range(1,25):
        try_page_link = main_link+f"/photos?page={pg}"
        pages.append(try_page_link)


    page = requests.get(main_link)
    soup = BeautifulSoup(page.content, 'html.parser')

    drama_name = soup.find('h1').get_text()
    txt_status.insert(END, f"\n\n{drama_name}")
    
    downloaded = []
    set_downloaded = False
    txt_status.insert(END, f"\n\nGetting download links...")
    for current_page in pages:
        page = requests.get(current_page)
        soup = BeautifulSoup(page.content, 'html.parser')

        drama_images = soup.find_all('a', class_='block')
        if set_downloaded==False:
            for drama_image in drama_images:
                drama_image_link = drama_image['href'].replace('/photos', 'https://i.mydramalist.com')+'.jpg'
                if drama_image_link in downloaded:
                    set_downloaded = True
                    break
                else:
                    downloaded.append(drama_image_link)
        else:
            break
        
            
            

    i = 0

    conf = messagebox.askyesno("Soju Downloader V1", f"There are total {len(downloaded)} files. \nDo you want to continue?")
    
    if conf==True:

        if os.path.exists(drama_name):
            messagebox.showerror("Soju Downloader V1", "Folder Exists. Download Cancelled!\nDelete the folder and try again.")
            txt_status.insert(END, f"Folder exists... Download Cancelled.")
        else: 
            os.mkdir(drama_name)
            txt_status.insert(END, f"\nStarting Download...\n")
            txt_status.insert(END, f"Directory created\n\n")  
            for j in downloaded:
                i+=1
                percentage = i/len(downloaded)
                r = requests.get(j, stream=True)
                if r.status_code == 200:        
                    txt_status.insert(END, f"[{i} of {len(downloaded)}] Downloading:  {j} {round(percentage*100, 2)} %\n")
                    txt_status.yview(END)
                    with open(f"{drama_name}/{drama_name} {i}.jpg", 'wb') as f:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, f)
            messagebox.showinfo("Soju Downloader V1", "All Photos Downloaded Successfully.")


    else:
        pass
    btn_search.configure(state=NORMAL)
    


root = Tk()
root.title("Soju-Downloader V1")
    

frm_search = Frame(root)
frm_search.grid(row=0, column=0, padx=10, pady=10)
lbl_search = Label(frm_search, text="Search for KDrama:", font=('consolas', 16))
lbl_search.grid(row=0, column=0, padx=10, pady=10)
ent_search = Entry(frm_search, width=20, font=('consolas', 12))
ent_search.grid(row=0, column=1, padx=10, pady=10)
btn_search = Button(frm_search, text="Search", command=lambda:threading.Thread(target=start_download).start())
btn_search.grid(row=0, column=2, padx=10, pady=10)

# root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='icon.png'))

frm_info = Frame(root, height=400, width=650)
frm_info.grid(row=1, column=0, padx=10, pady=10)
txt_status = Text(frm_info, height=5, fg="green", bg="black", wrap=WORD)
txt_status.grid(row=0, column=0)



root.mainloop()
