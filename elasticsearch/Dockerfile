# VERSION 1.0
# AUTHOR:         Pascal Grange
# DESCRIPTION:    risno/elasticsearch

FROM elasticsearch
MAINTAINER Pascal Grange

#Change data storage configuration so that it
#is not stored in the declared VOLUME of the
#elasticsearch base image. This way we can persist
#test data between containers.
RUN mkdir /usr/share/elasticsearch/data2
COPY elasticsearch.yml /usr/share/elasticsearch/config/

RUN mkdir /src
RUN mkdir /src/mappings

COPY ensure_elastic_running /src/
COPY mappings/tools /src/mappings/tools

WORKDIR /src/mappings

RUN echo "Injecting cities... this takes long !!!!!!!" >&2
COPY mappings/cities /src/mappings/cities
RUN /src/ensure_elastic_running &&\
    /bin/bash cities/inject_cities_in_elasticsearch.sh

# Inject other mappings
COPY mappings/ads /src/mappings/ads
RUN /src/ensure_elastic_running &&\
    /bin/bash ads/ads_1.0 &&\
    /bin/bash ads/ads_2.0 &&\
    /bin/bash ads/ads_2.1 &&\
    /bin/bash ads/ads_2.2

COPY mappings/types /src/mappings/types
RUN /src/ensure_elastic_running &&\
    /bin/bash types/types

COPY mappings/users /src/mappings/users
RUN /src/ensure_elastic_running &&\
    /bin/bash users/users_1.0

COPY mappings/utils /src/mappings/utils
RUN /src/ensure_elastic_running &&\
    /bin/bash utils/utils_0.1

RUN chown -R elasticsearch:elasticsearch /usr/share/elasticsearch/data2

# Define default command.
CMD ["/docker-entrypoint.sh"]

# Expose ports.
#   - 9200: HTTP
#   - 9300: transport
EXPOSE 9200
EXPOSE 9300

CMD ["elasticsearch"]
