# VERSION 1.0
# AUTHOR:         Pascal Grange <pascal@grange.nom.fr>
# DESCRIPTION:    risno/elasticsearch

FROM node:0.10.38
MAINTAINER Pascal Grange <pascal@grange.nom.fr>

RUN mkdir /src

ADD risno.json /etc/opt/risno.json
ADD . /src
WORKDIR /src
RUN npm install

EXPOSE 12043

CMD ["/usr/local/bin/node", "/src/index.js"]
