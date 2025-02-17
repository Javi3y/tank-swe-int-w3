import asyncio
from app.reservations.service.commands.reservation_queue import (
    resolve_reservation_command,
)
from app.unit_of_work import UnitOfWork
import json


async def reservation_queue_handler(payload: str, uow: UnitOfWork):
    payload_str = payload.decode("utf-8")
    payload_dict = json.loads(payload_str)
    try:
        print(payload_dict)
        resolve = await resolve_reservation_command(payload_dict["book"], uow)
        print(resolve)
        return resolve
    except Exception as e:
        pass


async def handle_reservation_queue_event(ch, method, properties, msg):
    async with UnitOfWork() as uow:
        resolve = await reservation_queue_handler(msg, uow)
        await uow.commit()
        return resolve


def handle_reservation_queue_event_sync(ch, method, properties, msg, main_loop):
    # Schedule the async callback on the main event loop
    asyncio.run_coroutine_threadsafe(
        handle_reservation_queue_event(ch, method, properties, msg), main_loop
    )
