# VERSION 1.0
# AUTHOR:         Nicolas Lamirault <nicolas.lamirault@gmail.com>
# DESCRIPTION:    risno/elasticsearch

FROM java:7
MAINTAINER Nicolas Lamirault <nicolas.lamirault@gmail.com>

ENV ES_VERSION 1.5.2

RUN apt-get -y update && apt-get install -y wget && apt-get clean

# Install Elasticsearch
RUN mkdir -p /src/elasticsearch && cd /src/elasticsearch && \
    wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-$ES_VERSION.tar.gz && \
    tar xzf elasticsearch-$ES_VERSION.tar.gz --strip-components=1 && \
    rm elasticsearch-$ES_VERSION.tar.gz && \
    /src/elasticsearch/bin/plugin -v -i mobz/elasticsearch-head && \
    /src/elasticsearch/bin/plugin -v -i royrusso/elasticsearch-HQ && \
    /src/elasticsearch/bin/plugin -v -i lmenezes/elasticsearch-kopf

ADD ./elasticsearch.yml /src/elasticsearch/elasticsearch.yml

VOLUME ["/var/lib/elasticsearch"]
VOLUME ["/var/log/elasticsearch"]

EXPOSE 9200
EXPOSE 9300

CMD ["/src/elasticsearch/bin/elasticsearch"]