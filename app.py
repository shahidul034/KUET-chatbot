from flask import Flask, redirect,render_template, request,redirect
from datetime import datetime
import logging
import sys
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import random
import string
import nltk
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


def greeting_response(text):
  text=text.lower()
  bot_greetings=['howdy','hi','hey','hello','hola']
  user_greetings=['hi','hey','hello','hola','greetings','wassup']
  for word in text.split():
    if word in user_greetings:
      return random.choice(bot_greetings)
def index_sort(list_var):
  length=len(list_var)
  list_index=list(range(0,length))
  x=list_var
  for i in range(length):
    for j in range(length):
      if x[list_index[i]] > x[list_index[j]]:
        temp=list_index[i]
        list_index[i]=list_index[j]
        list_index[j]=temp
  return list_index
def bot_response(user_input,sent_list):
  user_input=user_input.lower()
  sent_list.append(user_input)
  bot_response=''
  cm=CountVectorizer().fit_transform(sent_list)
  similarity_scores=cosine_similarity(cm[-1],cm)
  similarity_scores_list=similarity_scores.flatten()
  index=index_sort(similarity_scores_list)
  index=index[1:]
  response_flag=0
  j=0
  for i in range(len(index)):
    if similarity_scores_list[index[i]]>0.0:
      bot_response=bot_response +' ' +sent_list[index[i]]
      response_flag=1
      j+=1
    if j>2:
      break
  if response_flag==0:
    bot_response=bot_response+' '+"I apologize , I don't understand."
  sent_list.remove(user_input)
  return bot_response  
def searching(res,text):
   search1=re.search("\|\|.*\|\|", res)
   if search1:
      ans=(search1.group()).replace("|","")
      search_string="\|\|"+ans+"\|\|.*"+"[["+ans+"]]"
      search2 = re.search(search_string, text)
      if search2:
          msg=search2.group().replace("|","")
          msg=msg.replace("[","")
          msg=msg.replace("]","")
          msg=msg.replace(ans,"")
          return 1,msg
      else:
         return 0,""
   else:
      return 0,""
   
@app.route("/",methods=['GET','POST'])
def hello_world():
    nltk.download('punkt',quiet=True)
    # url = r'https://raw.githubusercontent.com/shahidul034/KUET-chatbot/main/Software-Project-Data.txt'
    # page = requests.get(url,verify=False)
    # corpus=page.text
    text=open(r"C:\Users\Inception\Desktop\python project dev\uttara chatbot\static\Software-Project-Data.txt","r",encoding="utf-8").read()
    sent_list=nltk.sent_tokenize(text)
    user_input=""
    msg=""
    print('Bot: I am bot. I will answer your queries about uttara university')
    exit_list=['exit','see you later','bye','quit','break']
    
    if request.method =='POST':
        user_input=(request.form['title'])
        if user_input.lower() in exit_list:
            msg="chat with you later !"
        else:
            if greeting_response(user_input)!=None:
                res=greeting_response(user_input)
                msg=res
            else:
                res=bot_response(user_input,sent_list)
                msg=res
                flag,out=searching(res,text)
                if flag:
                   msg=out
    return render_template("index.html",msg=msg)

if __name__ == "__main__":
    app.run(debug=True)