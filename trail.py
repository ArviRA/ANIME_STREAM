from bs4 import BeautifulSoup
import requests
from flask import Flask,request
app = Flask(__name__)

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


if __name__ == '__main__':
   app.run(debug = True)
    