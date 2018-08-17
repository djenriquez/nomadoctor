FROM python:3-slim
LABEL maintainer=dj@glympse.com

ENV APP_DIR=/opt/nomadoctor/

WORKDIR $APP_DIR
COPY ./requirements.txt $APP_DIR

RUN apt-get update \
    && pip install -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

COPY . $APP_DIR

ENTRYPOINT ["./main"]

CMD ["--help"]
