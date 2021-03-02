from bs4 import BeautifulSoup
import requests


def get_cover(name):
    result = requests.get('https://wallpapercave.com/{}-wallpapers'.format(name))
    soup = BeautifulSoup(result.content,'html.parser')
    if (len(soup.find_all('div',{'class':'wallpaper'}))!=0):
        dummy = soup.find_all('div',{'class':'wallpaper'})[0]
        cover = "https://wallpapercave.com/"+str(dummy.find('div',{'class':'fav'}).find('a').get('src'))
        #print(cover)
        return cover
    else:
        try:
            result = requests.get('https://wall.alphacoders.com/search.php?search={}'.format(name))
            soup = BeautifulSoup(result.content,'html.parser')
        #print(soup.find_all('div',{'class':'boxgrid'})[0].find('img').get('src'))
        #print(soup.prettify())
            return soup.find_all('div',{'class':'boxgrid'})[0].find('img').get('src')
        except:
            return 404