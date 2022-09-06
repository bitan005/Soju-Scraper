
# ![icon](https://user-images.githubusercontent.com/83669071/188553939-ca583f63-3d15-47f5-b77e-798ca3d8ed5b.png) Soju-Scraper


Soju-Scraper is a webscraping program to webscrape details and images from  [MyDramaList](https://www.mydramalist.com) website. 
Since there is no public API for this website, this project was made to webscrape directly from the website.

## Prerequisites

In order to run this program it is recommended to have at least **Python 3.6 or above**.

Also make sure that the following modules are installed:

- requests
- BeautifulSoup4
- Pillow
- tkscrolledframe

To install them at once, run:

``` pip install requests beautifulsoup4 pillow tkscrolledframe```


## Features
Along with a CLI interface (Coming Soon) it mainly has a easy-to-use GUI. It includes:

### Soju-Scraper
The main program used to display the info of any K-Drama along with the poster of it.
The UI is pretty simple and easy to use.
It displays **Name, Native Title, Popularity, Episodes, Airing Date, Synopsis and Cast** of the searched drama.
![Screenshot from 2022-09-06 03-34-18](https://user-images.githubusercontent.com/83669071/188554279-7a63c1c4-eb8d-41c5-bd28-784f4819901a.png)
![Screenshot from 2022-09-06 03-34-00(2)](https://user-images.githubusercontent.com/83669071/188554948-5d4fc08e-7ead-4429-adbd-b33a58213e4b.png)


Also it has a feature to show the **Top-100, Upcoming and Latest K-Dramas**.
![Toplevel Windows](https://user-images.githubusercontent.com/83669071/188554068-934877c4-29bd-4a79-a8ee-d6ca402289ae.png)

And the **About** button pops up a window which shows a little praise for me ;)

### Soju Downloader
Soju-Downloader is the program to download all the images of a drama from the MDL website.
It has a CLI interface for now and the GUI is still in development with a few bugs.
![video6104914364765046610](https://user-images.githubusercontent.com/83669071/188563833-1987f240-3ae3-46c9-ab1b-6c0a8c0a3445.gif)

It gets the image links and downloads them one-by-one and saves them in the same directory as of the porgram.



