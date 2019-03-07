FROM python:3.6.2-jessie

ENV PUSHOVER_TOKEN ""
ENV PUSHOVER_APP_KEY ""

ENV MSG_PREFIX ""
ENV WHITE_LIST ""
ENV BLACK_LIST ""
ENV LOGGING_LEVEL "INFO"
# seconds
ENV CHECK_INTERVAL "300"

USER root
WORKDIR /
ADD swarm-alert.py /swarm-alert.py
ADD swarm-alert.sh /swarm-alert.sh
ADD requirements.txt /requirements.txt

RUN chmod o+x /*.sh && chmod o+x /*.py && \
    pip install -r requirements.txt

ENTRYPOINT ["/swarm-alert.sh"]
