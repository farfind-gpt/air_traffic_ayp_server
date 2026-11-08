from app.models.countries import Country
from app.schemas.country_schemas import CountryNoIDShema
from app.schemas.count_shema import CountSchema
from app.controllers.countries_controller import CountriesController
from app.db.session import get_session
from app.api.rollback_on_exception import rollback_on_exception

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session


router = APIRouter(prefix="/countries", tags=["Countries"])


@router.get("", summary="get all countries")
def get_all_countries_route(session: Session = Depends(get_session)) -> list[Country]:
    return CountriesController.get_all(session)

@router.get("/{id}", summary="get country by id")
def get_country_by_id_route(id: int, session: Session = Depends(get_session)) -> Country:
    country = CountriesController.get_by_id(session, id)

    if country is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="not found")

    return country

@router.put("/{id}", summary="update country")
@rollback_on_exception
def update_country_route(id: int, country: CountryNoIDShema, session: Session = Depends(get_session)) -> Country:
    return CountriesController.update_country(session, id, country.name)

@router.post("", summary="add country")
@rollback_on_exception
def add_country_route(country: CountryNoIDShema, session: Session = Depends(get_session)) -> Country:
    return CountriesController.add_country(session, country.name)

@router.delete("/{id}", summary="delete country by id")
@rollback_on_exception
def delete_country_by_id_route(id: int, session: Session = Depends(get_session)) -> CountSchema:
    return CountSchema(count=(1 if CountriesController.delete_country(session, id) else 0))
