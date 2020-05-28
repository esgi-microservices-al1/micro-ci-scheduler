import os

from flask import request
from flask_restplus import Namespace, Resource

from dtos.MessageSenderDto import MessageSenderDto
from rabbitmq import receiver, sender

namespace = Namespace('communication', description='communication via amqp operations')


@namespace.route("/")
class Communication(Resource):

    def get(self):
        """
        Run the listener on the receiving queue
        """

        receiver.receive(os.environ['AMQP_IP'],
                         os.environ['AMQP_PORT'],
                         os.environ['AMQP_LOGIN'],
                         os.environ['AMQP_PWD'],
                         os.environ['AMQP_SEND_QUEUE'])

    @namespace.expect(str)
    def post(self):
        """
        Post messages to the sending queue
        """

        body = request.get_json()
        message_dto = MessageSenderDto.deserialize(body)
        valid_dto, error = message_dto.validate()
        if valid_dto is False:
            return error, 400

        message = message_dto.__getattribute__('message')

        sender.send(os.environ['AMQP_IP'],
                    os.environ['AMQP_PORT'],
                    os.environ['AMQP_LOGIN'],
                    os.environ['AMQP_PWD'],
                    os.environ['AMQP_SEND_QUEUE'],
                    message)
        return message
