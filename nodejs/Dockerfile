# VERSION 1.0
# AUTHOR:         Pascal Grange
# DESCRIPTION:    risno/risno-web

FROM node:0.10.38
MAINTAINER Pascal Grange

RUN mkdir /src

COPY package.json /src/
WORKDIR /src
RUN npm install

COPY . /src

EXPOSE 12043

CMD ["/usr/local/bin/node", "/src/index.js"]
