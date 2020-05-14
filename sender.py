#!/usr/bin/env python
import sys
import pika


def send(ip, port, login, pwd, queue, body):
    # ip = #192.168.1.94   // Where is rabbitmq installed
    # port = #5672           // Default port for AMQP

    # login =  #guest          // Default user
    # pwd =    #guest          // Default pwd

    # queue =   #hello          // The name of the queue

    # body =         #'Hello World'  // Message to sent to the queue

    credentials = pika.PlainCredentials(login, pwd)
    connection = pika.BlockingConnection(pika.ConnectionParameters(ip, port, '/', credentials))

    channel = connection.channel()

    channel.queue_declare(queue=queue)

    channel.basic_publish(exchange='',
                          routing_key=queue,
                          body=body)
    print(" [x] Sent " + body)


    connection.close()
