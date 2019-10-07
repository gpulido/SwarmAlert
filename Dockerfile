FROM python:3.6.2-jessie

ENV PUSHOVER_USER_KEY ""
ENV PUSHOVER_API_TOKEN ""

ENV MSG_PREFIX ""
ENV WHITE_LIST ""
ENV BLACK_LIST ""
ENV LOGGING_LEVEL "INFO"
# seconds
ENV CHECK_INTERVAL "300"

USER root

WORKDIR /

ADD requirements.txt /requirements.txt
RUN chmod o+x /*.sh && chmod o+x /*.py && \
    pip install -r requirements.txt

COPY ./src /src
ADD swarm-alert.sh /swarm-alert.sh


ENTRYPOINT ["/swarm-alert.sh"]
