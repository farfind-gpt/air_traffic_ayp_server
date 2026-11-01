from app.models.plane import Plane

from fastapi import HTTPException, status
from sqlmodel import Session, select, delete
from sqlalchemy.exc import IntegrityError


class PlanesController:

    @staticmethod
    def get_all(session: Session) -> list[Plane]:
        return list(session.exec(select(Plane)).all())

    @staticmethod
    def get_by_id(session: Session, id: int) -> Plane | None:
        return session.get(Plane, id)

    @staticmethod
    def add_plane(session: Session, name: str) -> Plane:
        search_res = session.exec(select(Plane).where(Plane.name == name)).first()

        if search_res:
            raise HTTPException(status.HTTP_409_CONFLICT, "plane with this name already exists")

        new_plane = Plane(name=name)

        session.add(new_plane)
        session.commit()
        session.refresh(new_plane)
        return new_plane

    @staticmethod
    def update_plane(session: Session, plane_id: int, name: str) -> Plane:
        plane = session.get(Plane, plane_id)

        if not plane:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "plane with this id not found")

        search_res = session.exec(select(Plane).where(Plane.name == name)).first()

        if search_res:
            raise HTTPException(status.HTTP_409_CONFLICT, "plane with this name already exists")

        plane.name = name

        session.add(plane)
        session.commit()
        session.refresh(plane)
        return plane

    @staticmethod
    def delete_plane(session: Session, plane_id: int) -> bool:
        plane: Plane | None = PlanesController.get_by_id(session, plane_id)

        if not plane:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "plane with this id not found")

        try:
            cnt: int = session.exec(delete(Plane).where(Plane.plane_id == plane_id)).rowcount
            session.commit()
            return cnt == 1
        except IntegrityError:
            raise HTTPException(status.HTTP_409_CONFLICT, "db integiry error, brobably the plane is used somewhere")
