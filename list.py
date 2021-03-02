from bs4 import BeautifulSoup
import requests
send = {}
raw_link = requests.get("https://gogo-play.net/")

#print(raw_link)
def tried():
    soup = BeautifulSoup(raw_link.content,"html.parser")

    dummy =soup.find_all('li',{'class':'video-block'})
    for i in range(0,len(dummy)):
        
        picture = dummy[i].find('div',{'class':'picture'})
        picture = picture.find('img')
        description = picture.get('alt')
        pic_link = picture.get('src')
        name = dummy[i].find('div',{'class':'name'}).text.strip()
        date = dummy[i].find('span',{'class':'date'}).text
        dummy_dic = {}
        dummy_dic['picture'] = pic_link
        dummy_dic['descripton'] = description
        dummy_dic['date'] = date
        dummy_dic["href"] = dummy[i].find('a').get('href')
        send[str(name)] = dummy_dic

    print(send)

def listed():
        raw = "https://gogo-play.net/videos/wave-surfing-yappe-tv-episode-8"
        send = {}
        raw_link = requests.get(raw)
        soup = BeautifulSoup(raw_link.content,"html.parser")
        ul = soup.find_all('ul',{'class':'listing items lists'})
        print(ul)
        dummy = ul[0].find_all('li',{'class':'video-block'})
        print(len(dummy))
        for i in range(0,len(dummy)):
            picture = dummy[i].find('div',{'class':'picture'})
            picture = picture.find('img')
            description = picture.get('alt')
            pic_link = picture.get('src')
            name = dummy[i].find('div',{'class':'name'}).text.strip()
            date = dummy[i].find('span',{'class':'date'}).text
            dummy_dic = {}
            dummy_dic['picture'] = pic_link
            dummy_dic['descripton'] = description
            dummy_dic['date'] = date
            dummy_dic["href"] = dummy[i].find('a').get('href')
            print(dummy_dic)
            send[str(name)] = dummy_dic
print(listed())