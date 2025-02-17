from contextlib import asynccontextmanager
from typing import List
from fastapi import Depends, FastAPI

from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.mappers import mapper
from app.adapters.postgres import get_db
from app.adapters.rabbitmq import RabbitMq
from app.adapters.redis import run_redis
from app.auth.entrypoints import auth
from sqlalchemy.orm import registry

from app.books.entrypoints import book
from app.reservations.entrypoints import reservation
from app.reservations.service.command_handlers.reservation_queue import (
    handle_reservation_queue_event_sync,
)
from app.users.domain.entities.user import User, UserOut
from app.users.entrypoints import author, client
import threading
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_generator = get_db()
    db = await anext(db_generator)
    mapper_registry = registry()
    metadata = mapper_registry.metadata
    main_loop = asyncio.get_event_loop()
    try:
        mapper(mapper_registry, metadata)
        app.state.n_client = await run_redis()
        await db.execute(text("create extension if not exists btree_gist;"))
        await db.commit()
        rabbitmq = RabbitMq()
        threading.Thread(
            target=lambda: rabbitmq.consume_messages(
                queue_name="reservation",
                callback=lambda ch, method, properties, msg: handle_reservation_queue_event_sync(
                    ch, method, properties, msg, main_loop
                ),
            ),
            daemon=True,
        ).start()
        yield
    finally:
        await db.close()
        await app.state.n_client.close()


app = FastAPI(lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=List[UserOut])
async def get_users(db: AsyncSession = Depends(get_db)):
    users = await db.execute(select(User))
    return {"users": users.scalars().all()}


app.include_router(client.router)
app.include_router(author.router)
app.include_router(auth.router)
app.include_router(book.router)
app.include_router(reservation.router)
