from datetime import UTC, datetime, timedelta
from typing import List

from fastapi import HTTPException
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from app.events.domain.entities.event import EventCreate
from app.events.domain.enums.event_type import EventTypeEnum
from app.reservations.domain.entities.reservation import Reservation, ReservationCreate
from app.reservations.domain.entities.reservation_queue import ReservationQueueCreate
from app.unit_of_work import UnitOfWork
from app.users.domain.enums.sub import SubEnum
from app.users.service.client import ClientService
import json


class ReservationService:
    pass
