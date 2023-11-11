FROM python:3.9-slim-buster
USER root
WORKDIR /root
ENV PYTHONPATH /root
RUN apt-get update && apt-get install build-essential -y
RUN apt-get install git -y
RUN pip install -U git+https://github.com/Future-Outlier/flytekit.git@0ecebdfc3a018d888748e4d9adf715c72c761180#subdirectory=plugins/flytekit-openai-chatgpt

RUN pip install -U git+https://github.com/Future-Outlier/flyte.git@b879137d24fe6bfb60d6d1182cd8d9b3f32335cc#subdirectory=flyteidl

RUN pip install -U git+https://github.com/Future-Outlier/flytekit.git@0ecebdfc3a018d888748e4d9adf715c72c761180


RUN pip install beautifulsoup4==4.12.2
RUN pip install gtts==2.4.0
RUN pip install openai==0.28.1
RUN pip install pytube==15.0.0
RUN pip install Requests==2.31.0
RUN pip install scrapetube==2.5.1
RUN pip install selenium==4.15.2
RUN pip install slack_sdk==3.23.0
RUN pip install tweepy==4.14.0
RUN pip install webdriver_manager==4.0.1
RUN pip install youtube_transcript_api==0.6.1
