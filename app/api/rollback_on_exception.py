from sqlmodel import Session

from typing import Callable, TypeVar, ParamSpec
import logging


logger = logging.getLogger(__name__)

T = TypeVar("T")
A = ParamSpec("A")


"""
decorator that rollbacks session on any exception
"""
def rollback_on_exception(func: Callable[A, T]) -> Callable[A, T]:
    def new_func(*args, **kwargs) -> T:
        session = kwargs.get("session", None)

        if not isinstance(session, Session):
            logger.error("session is not provided to function decorated with rollback_on_exception")
            return func(*args, **kwargs)

        try:
            return func(*args, **kwargs)
        except Exception:
            session.rollback()
            raise

    return new_func
