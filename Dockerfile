FROM linuxmintd/mint19.3-amd64
FROM python:3.6.9


#necessary rquirements for os

RUN apt-get -y update
RUN apt-get install -y libopenblas-dev liblapack-dev libatlas-base-dev
RUN apt-get install -y libx11-dev libgtk-3-dev
RUN apt-get -y update
RUN apt-get install -y python3-dev
RUN apt-get -y update

#Install chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable


#Installng chromedriver
RUN apt-get install -yqq unzip curl
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/


RUN mkdir /app
ADD . /app
WORKDIR /app


#Installing requirements
RUN apt-get install -y python3 python3-pip
RUN pip3 install -r req.txt

CMD python main.py
