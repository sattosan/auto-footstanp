FROM python:3.8

WORKDIR /usr/src
ADD requirements.txt ./
# requirements.txtにリストされたパッケージをインストールする
RUN pip install --trusted-host pypi.python.org -r requirements.txt