FROM python:3.9-slim-buster
USER root
WORKDIR /root
ENV PYTHONPATH /root
RUN apt-get update && apt-get install build-essential -y
RUN apt-get install git -y
RUN pip install -U git+https://github.com/Future-Outlier/flytekit.git@c19221a10f8c52da5924d7749b701ea2929c8aaf#subdirectory=plugins/flytekit-openai

RUN pip install -U git+https://github.com/Future-Outlier/flytekit.git@c19221a10f8c52da5924d7749b701ea2929c8aaf

RUN pip install beautifulsoup4==4.12.2
RUN pip install gtts==2.4.0
RUN pip install pytube==15.0.0
RUN pip install Requests==2.31.0
RUN pip install scrapetube==2.5.1
RUN pip install selenium==4.15.2
RUN pip install slack_sdk==3.23.0
RUN pip install tweepy==4.14.0
RUN pip install webdriver_manager==4.0.1
RUN pip install youtube_transcript_api==0.6.1
