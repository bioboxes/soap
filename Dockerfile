FROM ubuntu:latest
MAINTAINER Bioboxes

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y  wget

#install soap
RUN apt-get install soapdenovo2 -y

#install python 
RUN apt-get install python -y
RUN mkdir /opt/bin
RUN wget -O /opt/bin/PyYAML-3.11.tar.gz http://pyyaml.org/download/pyyaml/PyYAML-3.11.tar.gz
RUN tar xzvf /opt/bin/PyYAML-3.11.tar.gz -C /opt/bin
WORKDIR /opt/bin/PyYAML-3.11
RUN python setup.py install

#add schema, parser and run command 
ADD bbx/ /bbx
RUN apt-get install -y python-pip
RUN pip install jsonschema
RUN chmod a+x /bbx/run/default

ENV PATH /bbx/run:$PATH
