# Kuetbot

Kuetbot is a simple chatbot designed to answer questions about Khulna University of Engineering and Technology. It uses NLP to generate relevant responses and python flask as the GUI. The focus of this project was to build a bot where data could be added with little to no effort, without having to rewrite any code. 

## Prerequisites
- Python 3
- Flask==2.2.2
- nltk==3.7
- requests==2.28.1
- scikit_learn==1.2.1

## Download
You can download the Kuetbot by clicking [here](https://github.com/shahidul034/KUET-chatbot/archive/refs/heads/main.zip) or by cloning the project using the following command:

`git clone https://github.com/shahidul034/KUET-chatbot.git`

## How it works
Kuetbot uses the `CountVectorizer` from the `scikit-learn` library to convert the text data into a numerical representation, which is then used to calculate the cosine similarity between the user's input and the answers stored in the dataset. The answer with the highest cosine similarity is returned as the most relevant response.

The dataset is a slightly formatted text file, where new data can be added simply by appending it, following the established formatting.

## Screenshots
![Init](https://user-images.githubusercontent.com/49722623/229084528-6e572016-aedf-4f2b-8acd-3708783f3def.png)
![Query1](https://user-images.githubusercontent.com/49722623/229084558-8e27fbcc-8c8b-4915-91c1-efde02654fd6.png)
![Query3](https://user-images.githubusercontent.com/49722623/229086089-f7451e73-2f76-44ce-97a3-ce58cb6acb55.png)


## How to Use
- Clone or download the project
- Open the project in any Python IDE
- Run the `app.py` file located in the `KUETBOT` folder.

## Disclaimer
This is an alpha version of Kuetbot as proof of concept. expect bugs.
