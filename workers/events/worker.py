import asyncio
from config import settings

# from time import sleep
from asyncpg import connect
import json
import pika

rabbit_params = pika.ConnectionParameters(
    settings.rabbitmq_host,
    settings.rabbitmq_port,
    settings.rabbitmq_default_vhost,
    pika.PlainCredentials(settings.rabbitmq_username, settings.rabbitmq_password),
)


async def main():
    pika_connection = pika.BlockingConnection(rabbit_params)
    pika_channel = pika_connection.channel()
    pika_channel.queue_declare(queue="reservation")
    connection = await connect(
        user=settings.database_username,
        password=settings.database_password,
        database=settings.database_name,
        host=settings.database_host,
        port=settings.database_port,
    )
    try:
        while True:
            await asyncio.sleep(10)
            result = await connection.fetch(
                "SELECT * FROM event WHERE event_status = 'pending' AND timestamp >= now() AND timestamp <= now() + interval '61 seconds';"
            )
            for r in result:
                pika_channel.basic_publish(
                    exchange="",
                    routing_key="reservation",
                    body=json.dumps({**json.loads(r["payload"]), "event_id": r["id"]}),
                )
    finally:
        await connection.close()
        pika_connection.close()


asyncio.run(main())
