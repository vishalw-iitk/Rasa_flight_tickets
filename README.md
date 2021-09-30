# Rasa_flight_tickets
Mirafra's RASA Chatbot for booking flight tickets | flask backend

Steps to run:

Flights chatbot

1. export FLASK_APP=Flask/app.py
  - flask run --port 5000
2. rasa run --cors "*" --enable-api --model rasa_main/models --log-file rasa_main/story_graph.dot --endpoints rasa_main/endpoints.yml -p 5005
3. rasa run actions --actions rasa_main -p 5055

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
Python : 3.7.0
rasa: 2.8.6

Docker:
Docker should be installed.
Requirements.txt must be proper
docker-compose build
docker-compose up -d
docker-compose down