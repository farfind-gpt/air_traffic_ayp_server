from app.models.airline import Airline
from app.schemas.airline_schemas import AirlineNoIdShema
from app.schemas.count_shema import CountSchema
from app.controllers.airlines_controller import AirlinesController
from app.db.session import get_session

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session


router = APIRouter(prefix="/airlines", tags=["Airlines"])


@router.get("", summary="get all airlines")
def get_all_airlines_route(session: Session = Depends(get_session)) -> list[Airline]:
    from sqlalchemy.exc import IntegrityError
    raise IntegrityError("", None, Exception())
    return AirlinesController.get_all(session)

@router.get("/{id}", summary="get airline by id")
def get_airline_by_id_route(id: int, session: Session = Depends(get_session)) -> Airline:
    airline = AirlinesController.get_by_id(session, id)

    if airline is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="not found")

    return airline

@router.put("/{id}", summary="update airline")
def update_airline_route(id: int, data: AirlineNoIdShema, session: Session = Depends(get_session)) -> Airline:
    return AirlinesController.update_airline(session, id, data.name, data.airline_code)

@router.post("", summary="add airline")
def add_airline_route(airline: AirlineNoIdShema, session: Session = Depends(get_session)) -> Airline:
    return AirlinesController.add_airline(session, airline.airline_code, airline.name)

@router.delete("/{id}", summary="delete airline by id")
def delete_airline_by_id_route(id: int, session: Session = Depends(get_session)) -> CountSchema:
    return CountSchema(count=(1 if AirlinesController.delete_airline(session, id) else 0))
