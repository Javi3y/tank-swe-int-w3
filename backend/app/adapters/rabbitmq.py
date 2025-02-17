import pika
from app.config import settings

rabbit_params = pika.ConnectionParameters(
    settings.rabbitmq_host,
    settings.rabbitmq_port,
    settings.rabbitmq_default_vhost,
    pika.PlainCredentials(settings.rabbitmq_username, settings.rabbitmq_password),
)


class RabbitMq:
    def __init__(self):
        self.connection = pika.BlockingConnection(rabbit_params)
        self.channel = self.connection.channel()

    def declare(self, queue_name: str):
        self.channel.queue_declare(queue_name)

    def __exit__(self, *args, **kwargs):
        self.channel.close()

    def consume_messages(self, queue_name: str, callback):
        self.channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True
        )
        self.channel.start_consuming()

    def close_connection(self):
        self.connection.close()
