#!/usr/bin/env python
import sys
import pika


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
