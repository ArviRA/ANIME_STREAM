from bs4 import BeautifulSoup
import requests
from flask import Flask,request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/get_frame',methods = ['GET','POST'])
def get_link():
    try:
        print(request.args)
        link = dict(request.args)
        raw_link = link['raw_link']
        link = requests.get(raw_link)
        soup = BeautifulSoup(link.content,"html.parser")
        src = soup.find_all('iframe')
        add = "http:"+str(src[0]['src']).split('&')[0]
        return {'status':200,'link':add}
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
    