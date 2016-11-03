FROM ruimashita/scipy
ENV TERM xterm
MAINTAINER edanie15@gmail.com

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install supervisor
RUN apt-get install -y git unzip ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ADD requirements.txt /
RUN pip install -r requirements.txt

ADD dev-requirements.txt /
RUN pip install -r dev-requirements.txt

ADD .pypirc /root

RUN mkdir /lemmes
WORKDIR /lemmes
