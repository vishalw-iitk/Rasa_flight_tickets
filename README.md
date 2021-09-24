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
- name: vishal
- contact number: 9898989898
- From: mumbai
- To: london
- Date of onboarding: 12/32/32
- Boarding time: 34:43

Configs:
- Python version : 3.7
- rasa : 2.8.6