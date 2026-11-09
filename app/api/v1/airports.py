from app.models.airport import Airport
from app.schemas.airport_schemas import AirportNoIdSchema
from app.schemas.count_shema import CountSchema
from app.controllers.airports_controller import AirportsController
from app.db.session import get_session

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session


router = APIRouter(prefix="/airports", tags=["Airports"])


@router.get("", summary="get all airports")
def get_all_airports_route(session: Session = Depends(get_session)) -> list[Airport]:
    return AirportsController.get_all(session)

@router.get("/{id}", summary="get airport by id")
def get_airpotr_by_id_route(id: int, session: Session = Depends(get_session)) -> Airport:
    airport = AirportsController.get_by_id(session, id)

    if airport is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="not found")

    return airport

@router.put("/{id}", summary="update airport")
def update_airport_route(id: int, airport: AirportNoIdSchema, session: Session = Depends(get_session)) -> Airport:
    return AirportsController.update_airport(session, id, airport)

@router.post("", summary="add airport")
def add_airport_route(airport: AirportNoIdSchema, session: Session = Depends(get_session)) -> Airport:
    return AirportsController.add_airport(session, airport)

@router.delete("/{id}", summary="delete airport by id")
def delete_airport_by_id_route(id: int, session: Session = Depends(get_session)) -> CountSchema:
    return CountSchema(count=(1 if AirportsController.delete_airport(session, id) else 0))
