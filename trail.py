from bs4 import BeautifulSoup
import requests
from flask import Flask,request
from flask_cors import CORS
import images 

app = Flask(__name__)
CORS(app)

@app.route('/search_result',methods = ['GET','POST'])
def search():
    try:
        send = []
        link = dict(request.args)
        raw_link = link['raw_link']
        print(raw_link)
        link = requests.get(raw_link)
        print(link)
        soup = BeautifulSoup(link.content,"html.parser")
        
        dummy =soup.find_all('li',{'class':'video-block'})
        print(len(dummy))
        for i in range(0,len(dummy)):
            dummy_dict = {}
            picture = dummy[i].find('div',{'class':"picture"})
            picture  = picture.find('img')
            pic_link = picture.get('src')
            href = dummy[i].find('a').get('href')
            description = picture.get('alt')
            name = dummy[i].find('div',{'class':'name'}).text.strip()
            date = dummy[i].find('span',{'class':'date'}).text
            dummy_dict['href'] = href
            dummy_dict['pic_link']  =pic_link
            dummy_dict['description']  =description
            dummy_dict['name'] = name
            dummy_dict['date'] = date
            send.append(dummy_dict)
        #print(send)
        return {'status':200,'result':send}
    except:
        return {'status':404}

@app.route('/get_frame',methods = ['GET','POST'])
def get_link():
    try:
        list_dict = {}
        send = {}
        print(request.args)
        link = dict(request.args)
        raw_link = link['raw_link']
        link = requests.get(raw_link)
        soup = BeautifulSoup(link.content,"html.parser")
        ul = soup.find_all('ul',{'class':'listing items lists'})
        dummy = ul[0].find_all('li',{'class':'video-block'})
        for i in range(0,len(dummy)):
            dummy_dict = {}
            picture = dummy[i].find('div',{'class':"picture"})
            picture  = picture.find('img')
            pic_link = picture.get('src')
            href = dummy[i].find('a').get('href')
            description = picture.get('alt')
            name = dummy[i].find('div',{'class':'name'}).text.strip()
            date = dummy[i].find('span',{'class':'date'}).text
            dummy_dict['href'] = href
            dummy_dict['pic_link']  =pic_link
            dummy_dict['description']  =description
            dummy_dict['date'] = date
            list_dict[str(name)] = dummy_dict
        #print(list_dict)
        src = soup.find_all('iframe')
        cut_this = str(src[0]['src'])
        mp4 = cut_this[2:].replace("streaming","ajax")
        mp4 = mp4+"&refer="+raw_link
        print(mp4)
        send['frame_link']= "http:"+str(src[0]['src']).split('&')[0]
        print(cut_this.split('&')[1].split('+%')[0].split('=')[1].replace('+','-').replace('%3A',''))
        #print(cut_this.split('&')[1].split('+%')[0])
        details = soup.find("div",{'class':'video-details'})
        epi_name = details.find('span',{'class':'date'}).text.strip()
        epi_description = details.find('div',{'class':'content-more-js'}).text.strip()
        send['episode_name'] = epi_name
        send['epi_description'] = epi_description
        name = cut_this.split('&')[1].split('+%')[0].split('=')[1].replace('+','-').replace('%3A','')
        if len(name.split('-')) >=3:
            search_name  = name.split('-')[:2]
            separator = '-'
            name = separator.join(search_name)
        print("after:",name.lower())
        cover = images.get_cover(name.lower())
        print("cover",cover)
        
        return {'status':200,'in_this_frame':send,'below_episodes':list_dict,"mp4":mp4,'cover_pic':cover}
    except:
        return {'status':404}

@app.route('/get_list',methods = ['GET','POST'])
def get_list():
    try:
        print("inside")
        link = dict(request.args)
        raw = link['raw_link']
        send = {}
        raw_link = requests.get(raw)
        soup = BeautifulSoup(raw_link.content,"html.parser")
        dummy = soup.find_all('li',{'class':'video-block'})
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
        return {'status':200,'result':send}
    except:
        return {'status':404}
        




if __name__ == '__main__':
   app.run(debug = True)
    