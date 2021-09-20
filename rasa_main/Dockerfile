FROM rasa/rasa:2.8.6

USER root

RUN apt update

RUN python -m pip install --upgrade pip

COPY requirements.txt .

RUN pip3 install --no-cache -qr requirements.txt

RUN mkdir -p /usr/src/app/chatbot

WORKDIR /usr/src/app/chatbot

COPY . /usr/src/app/chatbot

USER 1001

# RUN flask run

# RUN rasa run actions

# ENTRYPOINT [ "--cors", '"*"'' --enable-api ]

# docker build -t flight_chatbot_rasa .
# docker run -it -p 5005:5005 flight_chatbot_rasa run --cors "*" --enable-api

# pip3 install rasa[spacy]
# rasa run --cors "*" --enable-api