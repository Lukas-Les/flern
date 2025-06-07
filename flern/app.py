import enum
import json

from datetime import datetime
from typing import Self

from dataclasses import dataclass
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.requests import Request
from starlette.routing import Route

from flern.db import create_or_return_connection 

DATE_TIME_FORMAT = "%d/%m/%Y %H:%M:%S"

async def health_check(request: Request) -> JSONResponse:
    conn = await create_or_return_connection()
    async with conn.cursor() as cursor:
        await cursor.execute("SELECT 1;")
        await cursor.fetchone()

        return JSONResponse({"status": "ok"})


async def homepage(request: Request) -> JSONResponse:
    return JSONResponse({'hello': 'world'})


class ActivityCategory(enum.Enum):
    consuming = "consuming" # eating food, drinking etc
    specialized_consuming = "specialized_consuming" # taking medicine, drugs etc
    action = "action" # sports, hike etc
    illness = "illness"


@dataclass
class Activity:
    start_date: datetime | None
    end_date: datetime | None
    exact_date: datetime | None

    category: ActivityCategory 
    act: str
    comment: str | None

    @classmethod
    def from_response_body(cls, body: bytes) -> Self:
        body_json = json.loads(body.decode())
        start_date_str = body_json.get("startDate")
        end_date_str = body_json.get("endDate")
        exact_date_str = body_json.get("exactDate")

        start_date = datetime.strptime(start_date_str, DATE_TIME_FORMAT)
        end_date = datetime.strptime(end_date_str, DATE_TIME_FORMAT)
        exact_date = datetime.strptime(exact_date_str, DATE_TIME_FORMAT)

        return cls(
            start_date=start_date,
            end_date=end_date,
            exact_date=exact_date,
            category=body_json.get("category"),
            act=body_json.get("act"),
            comment=body_json.get("comment"),
        )


async def activity(request: Request) -> JSONResponse:
    activity = Activity.from_response_body(await request.body())
    print(activity)
    return JSONResponse({"activity accepted"})
    

app = Starlette(debug=True, routes=[
    Route('/', homepage),
    Route("/health", health_check)
])
