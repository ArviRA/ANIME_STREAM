from bs4 import BeautifulSoup
import requests
from flask import Flask,request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
        dummy =soup.find_all('li',{'class':'video-block'})
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
        send['frame_link']= "http:"+str(src[0]['src']).split('&')[0]
        details = soup.find("div",{'class':'video-details'})
        epi_name = details.find('span',{'class':'date'}).text.strip()
        epi_description = details.find('div',{'class':'content-more-js'}).text.strip()
        send['episode_name'] = epi_name
        send['episode_description'] = epi_description
        return {'status':200,'in_this_frame':send,'below_episodes':list_dict}
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
        return {'status':200,'result':send}
    except:
        return {'status':404}
        




if __name__ == '__main__':
   app.run(debug = True)
    