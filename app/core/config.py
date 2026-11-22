from app.utils.passwords import is_weak

import os

from dotenv import load_dotenv


load_dotenv()

_db_url_env: str | None = os.getenv("DATABASE_URL")
DATABASE_URL: str = _db_url_env if _db_url_env else ""

if not (JWK := os.getenv("JWK")):
    err_type = ValueError if isinstance(JWK, str) else TypeError
    raise err_type("no valid JWK provided in .env file")

ADMIN_NAME = os.getenv("ADMIN_NAME")
ADMIN_PWD = os.getenv("ADMIN_PWD")

if ADMIN_NAME is not None:
    if ADMIN_PWD is None:
        raise RuntimeError("config error: config error: ADMIN_NAME is present but ADMIN_PWD is not, add ADMIN_PWD env var or remove ADMIN_NAME")

    if reason := is_weak(ADMIN_PWD):
        raise ValueError(f"ADMIN_PWD is weak: {reason}")

    if ADMIN_NAME == "":
        raise ValueError("config error: ADMIN_NAME cannot be empty")
elif ADMIN_PWD is not None:
    raise RuntimeError("config error: ADMIN_PWD is present but ADMIN_NAME is not, add ADMIN_NAME env var or remove ADMIN_PWD")

PAGE_LIMIT: int = 50
