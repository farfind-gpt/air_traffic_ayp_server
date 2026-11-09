from sqlmodel import Session

from app.db.database import ENGINE

import logging


logger = logging.getLogger(__name__)


def get_session():
    with Session(ENGINE) as session:
        try:
            yield session
        except Exception:
            logger.error("exception within session: rolling back", stack_info=True)
            session.rollback()
            raise
        finally:
            session.close()
