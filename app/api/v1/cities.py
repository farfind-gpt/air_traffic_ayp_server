from app.models.city import City
from app.schemas.city_shemas import CityNoIDSchema
from app.schemas.count_shema import CountSchema
from app.controllers.cities_controller import CitiesController
from app.db.session import get_session
from app.api.rollback_on_exception import rollback_on_exception

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session


router = APIRouter(prefix="/citites", tags=["Cities"])


@router.get("", summary="get all cities")
def get_all_cities_route(session: Session = Depends(get_session)) -> list[City]:
    return CitiesController.get_all(session)

@router.get("/{id}", summary="get city by id")
def get_cities_by_id_route(id: int, session: Session = Depends(get_session)) -> City:
    city = CitiesController.get_by_id(session, id)

    if city is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="not found")

    return city

@router.put("/{id}", summary="update city")
@rollback_on_exception
def update_city_route(id: int, city: CityNoIDSchema, session: Session = Depends(get_session)) -> City:
    return CitiesController.update_city(session, id, city)

@router.post("", summary="add city")
@rollback_on_exception
def add_city_route(city: CityNoIDSchema, session: Session = Depends(get_session)) -> City:
    return CitiesController.add_city(session, city.name, city.fk_country_id)

@router.delete("/{id}", summary="delete country by id")
@rollback_on_exception
def delete_city_by_id_route(id: int, session: Session = Depends(get_session)) -> CountSchema:
    return CountSchema(count=(1 if CitiesController.delete_city(session, id) else 0))
