FROM python:3.12.0-bullseye

# mirror ustc 
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list

RUN apt update && apt upgrade -y;
RUN apt install -y python3-pip;
# mysql client 
RUN apt install -y default-libmysqlclient-dev;
# uwsgi 
# RUN apt install -y uwsgi;

# pip mirror ustc 
RUN mkdir -p ~/.pip;
RUN echo "[global]" >> ~/.pip/pip.conf;
RUN echo "index-url = https://mirrors.ustc.edu.cn/pypi/web/simple" >> ~/.pip/pip.conf;
RUN echo "[install]" >> ~/.pip/pip.conf;
RUN echo "trusted-host=mirrors.ustc.edu.cn" >> ~/.pip/pip.conf;


RUN pip3 install --upgrade pip;
COPY . /app
WORKDIR /app
RUN pip3 install uwsgi;
# pip install 
RUN pip3 install -r requirements.txt;
ENV PYTHONPATH=/app
