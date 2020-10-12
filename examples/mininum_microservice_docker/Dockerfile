FROM python:3.6.4-alpine3.7

RUN apk add --update curl gcc g++ git libffi-dev openssl-dev python3-dev build-base linux-headers \
    && rm -rf /var/cache/apk/*

ENV PYTHONUNBUFFERED=1 APP_HOME=/microservice/
ENV PYMS_CONFIGMAP_FILE="$APP_HOME"config-docker.yml

RUN mkdir $APP_HOME && adduser -S -D -H python
RUN chown -R python $APP_HOME
WORKDIR $APP_HOME

RUN pip install --upgrade pip
RUN pip install -r py-ms gunicorn gevent


ADD . $APP_HOME

EXPOSE 5000
USER python

CMD ["gunicorn", "--worker-class", "gevent", "--workers", "8", "--log-level", "INFO", "--bind", "0.0.0.0:5000", "manage:app"]