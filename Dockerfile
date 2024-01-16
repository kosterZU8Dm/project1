FROM python:3.12.1-alpine3.19.0
LABEL maintainer="kostochka11@proton.me"

ARG WORK_DIR=/opt/project1
USER root
RUN mkdir -p $WORK_DIR
WORKDIR $WORK_DIR
COPY ./* .
RUN apk add libpq-dev && pip3 install -r requirements.txt
ENTRYPOINT ["gunicorn"]
CMD ["-w 4", "-b 0.0.0.0:8000", "app:app"]
