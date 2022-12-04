#render template renders html from render folder
from flask import Flask,render_template
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk, os, sys
import requests,re

#pyinstaller C:\Users\Administrator\Documents\Work\KUET-chatbot\KUETBOT\app.py --add-data "C:\Users\Administrator\Documents\Work\KUET-chatbot\KUETBOT\templates;templates" --add-data "C:\Users\Administrator\Documents\Work\KUET-chatbot\KUETBOT\static;static"

#new instance of flask
if getattr(sys, 'frozen', False):
    # we are running in a bundle, base folder in executable is sys._MEIPASS
    bundle_dir = sys._MEIPASS
    template_folder = bundle_dir + '/templates'
    static_folder = bundle_dir + '/static'
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    # we are running in a normal Python environment
    bundle_dir = os.path.dirname(os.path.abspath(__file__))
    app = Flask(__name__)


#global list
sentenceList = nltk.sent_tokenize("demo")
fullText="demo"


#app.route gives the webpage where this functioni will be [triggered],
#in this case, "/" or home page
#if a route has post or get forms, needs to be defined
@app.route("/", methods=['GET','POST'])
def hello_world():
    #nltk.download('punkt')
    sentenceUpdate()
    app.debug = True
    return render_template('index.html')

#this is called by javascript to get response
@app.route("/botResponse/<userText>", methods=['GET','POST'])
def botResponse(userText):
    #print("MainFunction",file=sys.stderr)
    sentenceList.append(userText)
    bot_response=''
    cm=CountVectorizer(stop_words='english').fit_transform(sentenceList)
    similarity_scores=cosine_similarity(cm[-1],cm)
    similarity_scores_list=similarity_scores.flatten()
    index=index_sort(similarity_scores_list)
    
    index=index[1:]
    
    response_flag=0
    j=0
    for i in range(len(index)):
        if similarity_scores_list[index[i]]>0.0:
            bot_response=bot_response+sentenceList[index[i]]
            response_flag=1
            j+=1
        if j>0:
            #j limits the number of results, 0 = only the first result
            break
    if response_flag==0:
        bot_response=bot_response+' '+"I apologize, I don't understand."
    else:
        flag,out=searching(bot_response,fullText)
        if flag:
            bot_response=out
    sentenceList.remove(userText)
    return bot_response    

#Updates sentence main sentence list
def sentenceUpdate():
    url= r'https://raw.githubusercontent.com/shahidul034/KUET-chatbot/main/KUETBOT/static/Software-Project-Data.txt'
    page = requests.get(url)
    global fullText
    fullText = page.text
    #fullText = open(r"C:\\Users\Administrator\Documents\Work\KUET-chatbot\KUETBOT\static\Software-Project-Data.txt",encoding="utf8").read()
    global sentenceList
    #sentenceList = nltk.sent_tokenize(text)
    sentenceList = fullText.split(" /")

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

#Checks for complete Regular expression blocks
def searching(botResponse,fullText):
    #print("In the link",file=sys.stderr)
    #search for occurence of block start
    search1=re.search("//.*//", botResponse)
    ####fix here####
    if search1:
        ans=search1.group()
        #print(ans,file=sys.stderr)
        ans= ans.replace("/","")
        #print(ans,file=sys.stderr)
        #search_string="//"+ans+"//"+"(.*\n)*"+"\[\["+ans+"\]\]"
        search_string = '(//'+ans+'//)(.+)((?:\n.+)+)(\[\['+ans+'\]\])'
        #search for whole block including block end
        search2 = re.search(search_string, fullText,re.MULTILINE)
        if search2:
            msg=search2.group()
            #print(msg+" foundsearch2",file=sys.stderr)
            msg=re.sub("//.*//","",msg)
            msg=re.sub("\[\[.*\]\]","",msg)
            msg.replace(" /","")
            #print(msg,file=sys.stderr)
            return 1,msg
        else:
            #print("notfound2",file=sys.stderr)
            return 0,"" 
    else:
        #start block not found, replacing end block if exists
        #print("found end with no start",file=sys.stderr)
        botResponse=re.sub("\[\[.*\]\]","",botResponse)
        return 1,botResponse

if __name__ == "__main__":
    app.run(debug=True)
