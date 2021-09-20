FROM python:alpine3.7

RUN python -m pip install --upgrade pip

COPY requirements.txt .

RUN pip3 install --no-cache -qr requirements.txt

RUN mkdir -p /usr/src/app/chatbot

WORKDIR /usr/src/app/chatbot

COPY . /usr/src/app/chatbot

EXPOSE 5000

# RUN flask run {NOT WORKING}
# RUN python app.py

# RUN rasa run actions

# ENTRYPOINT [ "--cors", '"*"'' --enable-api ]

# docker build -t flight_flask .
# docker run -it -p 5000:5000 flight_flask python app.py
