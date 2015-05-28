FROM node:0.10.38

RUN mkdir /src

ADD risno.json /etc/risno.json
ADD . /src
WORKDIR /src
RUN npm install

EXPOSE 12043

CMD ["/usr/bin/node", "src/index.js"]
