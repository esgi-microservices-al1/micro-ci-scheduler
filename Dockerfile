FROM python:3.7
COPY . /app
WORKDIR /app

ARG DB_USER
ARG DB_PWD
ARG DB_HOST
ARG DB_NAME
ARG DB_URI

ARG AMQP_IP
ARG AMQP_PORT
ARG AMQP_LOGIN
ARG AMQP_PWD
ARG AMQP_SEND_QUEUE

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install 'pymongo[srv]'

EXPOSE 5000

# RUN groupadd -g 999 appuser && useradd -r -u 999 -g appuser appuser

CMD ["python", "app.py"]
# CMD ["flask","run", "--host=0.0.0.0"]