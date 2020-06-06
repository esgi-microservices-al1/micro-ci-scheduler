import os
import sys
import pika
import argparse


def send(ip, port, login, pwd, queue, body):
    credentials = pika.PlainCredentials(login, pwd)
    connection = pika.BlockingConnection(pika.ConnectionParameters(ip, port, '/', credentials))

    channel = connection.channel()

    channel.queue_declare(queue=queue)

    channel.basic_publish(exchange='',
                          routing_key=queue,
                          body=body)
    print(" [x] Sent " + body)

    connection.close()


print('time to build, message to send = ' + sys.argv[0])

parser = argparse.ArgumentParser(description='test script')
parser.add_argument('--message', type=str, required=True,
                    help='message')
args = parser.parse_args()

send(os.environ['AMQP_IP'],
     os.environ['AMQP_PORT'],
     os.environ['AMQP_LOGIN'],
     os.environ['AMQP_PWD'],
     os.environ['AMQP_SEND_QUEUE'],
     args.message)
