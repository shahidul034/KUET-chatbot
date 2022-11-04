#render template renders html from render folder
from flask import Flask, render_template, request, jsonify

#new instance of flask
app = Flask(__name__)

#app.route gives the webpage where this functioni will be triggered,
#in this case, "/" or home page
#if a route has post or get forms, needs to be defined
@app.route("/", methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        print("post")
    return render_template('index.html')

@app.route("/botResponse")
def botResponse():
    return jsonify({"placeholder"})

if __name__ == "__main__":
    app.run(debug=True)
