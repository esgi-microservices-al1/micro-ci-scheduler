FROM python:3.7
WORKDIR /app
COPY . /app

ARG DB_USER
ARG DB_PWD
ARG DB_HOST
ARG DB_NAME

ARG AMQP_IP
ARG AMQP_PORT
ARG AMQP_LOGIN
ARG AMQP_PWD
ARG AMQP_SEND_QUEUE

RUN pip install -r requirements.txt
RUN pip install 'pymongo[srv]'

EXPOSE 5000

CMD ["flask","run", "--host=0.0.0.0"]