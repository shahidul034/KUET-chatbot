#render template renders html from render folder
from flask import Flask,render_template
import sys
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk, os, sys
import requests

#new instance of flask
if getattr(sys, 'frozen', False):
    # we are running in a bundle
    bundle_dir = sys._MEIPASS
    template_folder = bundle_dir + '/templates'
    static_folder = bundle_dir + '/static'
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    # we are running in a normal Python environment
    bundle_dir = os.path.dirname(os.path.abspath(__file__))


#global list
sentenceList = nltk.sent_tokenize("demo")


#app.route gives the webpage where this functioni will be [triggered],
#in this case, "/" or home page
#if a route has post or get forms, needs to be defined
@app.route("/", methods=['GET','POST'])
def hello_world():
    #nltk.download('punkt')
    sentenceUpdate()
    return render_template('index.html')

#this is called by javascript to get response
@app.route("/botResponse/<userText>", methods=['GET','POST'])
def botResponse(userText):
    #sentenceUpdate()
    sentenceList.append(userText)
    bot_response=''
    cm=CountVectorizer().fit_transform(sentenceList)
    similarity_scores=cosine_similarity(cm[-1],cm)
    similarity_scores_list=similarity_scores.flatten()
    index=index_sort(similarity_scores_list)
    index=index[1:]
    response_flag=0
    j=0
    for i in range(len(index)):
        if similarity_scores_list[index[i]]>0.0:
            bot_response=bot_response +' ' +sentenceList[index[i]]
            response_flag=1
            j+=1
        if j>2:
            break
    if response_flag==0:
        bot_response=bot_response+' '+"I apologize, I don't understand."
    sentenceList.remove(userText)
    return bot_response  

#Updates sentence main sentence list
def sentenceUpdate():
    url= r'https://raw.githubusercontent.com/shahidul034/KUET-chatbot/KUETBOT/KUETBOT/static/Software-Project-Data.txt'
    page = requests.get(url)
    text = page.text
    global sentenceList
    sentenceList = nltk.sent_tokenize(text)

#sorting method for sorting result quality
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


if __name__ == "__main__":
    app.run(debug=True)
