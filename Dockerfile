# Start with Ubuntu base image
FROM ubuntu:14.04
MAINTAINER Mark Wang <peiqi1122@gmail.com>

RUN echo "deb http://archive.ubuntu.com/ubuntu/ $(lsb_release -sc) main universe" >> /etc/apt/sources.list

# Install build-essential, git, wget, python-dev, pip and other dependencies
RUN apt-get update && apt-get install -y \
  tar \
  nano \
  curl \
  net-tools \
  build-essential \
  git \
  wget \
  libopenblas-dev \
  python \
  python-dev \
  python-pip \
  python-nose \
  python-numpy \
  python-scipy

# Install bleeding-edge Theano
RUN pip install --upgrade --no-deps git+git://github.com/Theano/Theano.git
RUN pip install dota2api


RUN git clone https://github.com/tt6746690/iGEM2016.git

EXPOSE 80
WORKDIR /iGEM2016/dota2DL
CMD pwd
