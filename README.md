# Rasa_flight_tickets
Mirafra's RASA Chatbot for booking flight tickets | flask backend

Steps to run:

rasa train

Working directory should contain the following :
1. Flask folder
2. Rasa folder
3. .dockerignore
4. .env
5. .gitignore


Flights chatbot

1. export FLASK_APP=Flask/app.py
  - flask run --port 5000
2. rasa run --cors "*" --enable-api --model Rasa/rasa_main/models --log-file Rasa/rasa_main/story_graph.dot --endpoints Rasa/rasa_main/endpoints.yml -p 5005
3. rasa run actions --actions Rasa/rasa_main -p 5055

or

1. python app.py
2. rasa run --cors "*" --enable-api
3. rasa run actions

Sample flight ticket requirements:
- name: Vishal
- contact number: 9898989898
- From: mumbai
- To: london
- departueDate: 2021-11-10
- returnDate: 2021-11-11 
- nonstop: false
- budget: 300000


Virtual environemnt: Without docker

action_endpoint:
 url: "http://localhost:5055/webhook"

Two requirements.txt files : 1 in Flask folder and 2nd in Rasa folder

Python : 3.7.0
rasa: 2.8.6
spacy: 3.1.3
rasa-sdk: 2.8.2
python-dotenv 0.19.0
rasa : pip: 21.1.3
rasa : setuptools 54.2.0
rasa : wheel : 0.36.2
flask : pip  21.2.4
flask : setuptools 57.4.0
flask : wheel 0.37.0



Docker:
Docker should be installed.
In endpoints.yml :
action_endpoint:
 url: "http://rasa_action_server:5055/webhook"

docker-compose build
docker-compose --env-file .env up