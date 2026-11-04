from app.db.database import create_db, close_db

from app.api.v1.cities import router as cities_router
from app.api.v1.countries import router as countries_router
from app.api.v1.passport_info import router as passport_info_router

from app.models.airline import Airline
from app.models.airport import Airport
from app.models.flight import Flight
from app.models.plane import Plane
from app.models.plane_seat import PlaneSeat
from app.models.reservation import Reservation
from app.models.reservation_group import ReservationGroup
from app.models.reservation_request import ReservationRequest
from app.models.user import User

from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from sqlalchemy.exc import IntegrityError
import uvicorn

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield
    close_db()


app_v1 = FastAPI(lifespan=lifespan)

# why this doesn't work correctly
@app_v1.exception_handler(Exception)
async def default_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, (HTTPException, RequestValidationError)):
        raise exc
    elif isinstance(exc, IntegrityError):
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "probably this request provided data that violates database integrity, but it was not properly handled by the server")
    else:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"internal error: {type(exc).__name__}")

for router in [cities_router, countries_router, passport_info_router]:
    app_v1.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app_v1)
