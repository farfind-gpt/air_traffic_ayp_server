from app.core.config import DATABASE_URL

from sqlmodel import SQLModel, create_engine
from app.controllers.cities_controller import *
from app.controllers.countries_controller import *
from app.controllers.passport_info_controller import *
from app.controllers.planes_controller import *


ENGINE = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True, pool_recycle=3600)

"""
creates database
"""
def create_db():
    SQLModel.metadata.create_all(ENGINE)

# TODO: ?
"""
closes database
"""
def close_db():
    ENGINE.dispose()
