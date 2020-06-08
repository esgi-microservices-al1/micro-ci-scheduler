"""
Prérequis pour le fonctionnement de ce script sur une machine linux :
 - Python 2.7 ou plus récent
 - pip installé pour tous les users (curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && sudo python get_pyp.py)
"""
import os
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


parser = argparse.ArgumentParser(description='send build order script')
parser.add_argument('--message', type=str, required=True,
                    help='message')
args = parser.parse_args()

print('time to build, message to send = ' + args.message)

send(os.environ['AMQP_IP'].rstrip(),
     os.environ['AMQP_PORT'].rstrip(),
     os.environ['AMQP_LOGIN'].rstrip(),
     os.environ['AMQP_PWD'].rstrip(),
     os.environ['AMQP_SEND_QUEUE'].rstrip(),
     args.message)
