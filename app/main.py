from app.db.database import create_db, close_db
from app.db.session import get_session

from app.api.v1.airlines import router as airlines_router
from app.api.v1.airports import router as airports_router
from app.api.v1.cities import router as cities_router
from app.api.v1.countries import router as countries_router
from app.api.v1.planes import router as planes_router
from app.api.v1.passengers import router as passengers_router
from app.api.v1.reservation_groups import router as reservation_groups_router
from app.api.v1.flights import router as flights_router
from app.api.v1.users import router as users_router
from app.api.v1.auth import router as auth_router

from app.controllers.users_controller import UsersController

from app.models.reservation import Reservation

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
import uvicorn

from contextlib import asynccontextmanager, contextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    with contextmanager(get_session)() as session:
        UsersController.on_startup(session)
    yield
    close_db()


app_v1 = FastAPI(lifespan=lifespan)

@app_v1.exception_handler(IntegrityError)
async def default_exception_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "probably this request provided data that violates database integrity, but it was not properly handled by the server"
        }
    )

for router in [airlines_router, airports_router, cities_router, countries_router, planes_router, passengers_router, reservation_groups_router, flights_router, users_router, auth_router]:
    app_v1.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app_v1)
