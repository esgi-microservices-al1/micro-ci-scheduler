#!/usr/bin/env python
import pika


def receive(ip, port, login, pwd, queue):
    credentials = pika.PlainCredentials(login, pwd)

    connection = pika.BlockingConnection(pika.ConnectionParameters(ip, port, '/', credentials))

    channel = connection.channel()

    channel.queue_declare(queue=queue)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        """
        run a scheduler form body
        """
        return body

    channel.basic_consume(queue=queue,
                          auto_ack=True,
                          on_message_callback=callback)

    print('[x] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
