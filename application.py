from flask import Flask, request
import requests
from bs4 import BeautifulSoup as bs
import urllib
from twilio.twiml.messaging_response import MessagingResponse
from random import randint
import gspread
import datetime
from oauth2client.service_account import ServiceAccountCredentials
import gif
import taskList
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('picografix-595144570179.json')
client = gspread.authorize(creds)
sheet = client.open('DataBase Whatsapp').sheet1
app = Flask(__name__)
@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    incoming_num1 = request.values.get('To', '').lower() #although not necessary but still
    incoming_num2  = request.values.get('From', '').lower()#the incoming message mobile number
    current = str(datetime.datetime.now())  
    resp = MessagingResponse()
    msg = resp.message()
    completionMsg = "" #this is to store the displayed result
    responded = False
    if 'quote' in incoming_msg:
        # return a quote
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        msg.body(quote)
        responded = True
        completionMsg = quote
    if 'cat' in incoming_msg:
        # return a cat pic
        msg.body('I love cats')
        msg.media('https://cataas.com/cat')
        responded = True
        completionMsg = 'https://cataas.com/cat'
    if 'dog' in incoming_msg:
        # return a cat pic
        responseDog=requests.get("https://dog.ceo/api/breeds/image/random")
        l = responseDog.json()
        ans = l['message']
        msg.body('Love <3')
        msg.media(ans)
        responded = True
        completionMsg = ans
    if 'wallpaper' in incoming_msg:
        l=incoming_message.split()
        url=l[1]
        try: 
            from googlesearch import search 
        except ImportError:  
            print("No module named 'google' found") 
            completionMsg = "No module named 'google' found"
        # to search 
        query = url+" unsplash"
        for j in search(query, tld="co.in", num=1, stop=4, pause=2):
            if "https://unsplash.com/s/photos" in j: 
                url=j 
        a=urllib.request.urlopen(url,context=ctx).read()
        soup=bs(a,'html.parser')
        L=soup.find_all('a',{'title':"Download photo"})
        x=randint(1,len(L)-1)
        alink=L[x].get('href')
        msg.media(alink)
        completionMsg=alink
        responded=True
    if 'unsplash' in incoming_msg:
         # return a cat pic
        msg.body('Here You Go ')
        un_img = 'https://source.unsplash.com/random'
        msg.media(un_img)
        responded = True
        completionMsg = un_img
    if 'spam' in incoming_msg:
         # spams 
        l = incoming_msg.split()
        countSpam = int(l[1])
        mess = " ".join(l[2:])
        for i in range(countSpam):
            msg.body(mess)
        completionMsg = "Succesfully spammed"
        responded = True
    if 'dank-joke' in incoming_msg:
        #sends a random dank joke
        responseDog=requests.get("https://sv443.net/jokeapi/v2/joke/Any?type=single")
        l = responseDog.json()
        msg.body(l['joke'])
        completionMsg = l['joke']
        responded = True
    if 'dict' in incoming_msg:
        headersDict = {    'Authorization': 'Token e3d0b4298a9592eb23efa0419b031d2ffadc94d4',
            }
        urlForDict = 'https://owlbot.info/api/v4/dictionary/'
        incoming_msg = 'dict cat'
        l = incoming_msg.split()
        searchTerm = l[1]
        urlForDict += searchTerm
        response = requests.get(urlForDict, headers=headersDict)
        ans = response.json()
        pronounciation = ans['pronunciation']
        defination = ans['definitions'][0]['definition']
        img = ans['definitions'][0]['image_url']
        example = ans['definitions'][0]['example']
        returnString = "*Defination* : " + defination + "\n" + "*usage*: " + example
        msg.body(returnString)
        msg.media(img)  
        completionMsg="successfully sent"
        responded = True
    if 'que' in incoming_msg:
        import urllib.request, urllib.parse, urllib.error
        import xml.etree.ElementTree as ET
        import ssl
        from bs4 import BeautifulSoup as bs

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        url = ' '.join(incoming_msg.split()[1:])

        try: 
            from googlesearch import search 
        except ImportError:  
            print("No module named 'google' found") 
          
        # to search 
        query = url+" stackoverflow"
          
        for j in search(query, tld="co.in", num=1, stop=1, pause=2): 
            url=j 
        a=urllib.request.urlopen(url,context=ctx).read()
        soup=bs(a,'html.parser')
        L=soup.find_all('div',{'class':'post-text'})
        i=L[1]
        msg.body(i.text)
        print(i.text)
        completionMsg = i.text
        responded = True
    if 'task' in incoming_msg:
        l = incoming_msg.split()
        mess = " ".join(l[2:])
        taskList.addTask(mess)
        msg.body("Successfully Added Your Task")
        completionMsg = "Successfully Added Your Task"
        responded = True
    if not responded:
        media_url = gif.give_url(incoming_msg)
        msg.body(media_url)
        msg.body('I only know about famous quotes and cats, sorry! (ver 1.0.2)')
        completionMsg ="returned deefault value"
    row = [current,incoming_num1,incoming_num2,incoming_msg,completionMsg]
    sheet.insert_row(row,index=2)
    return str(resp)

@app.route('/')
def index():
    return "hello this is my whatsapp bot"
if __name__ == '__main__':
    app.run()
