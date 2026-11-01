import os

from dotenv import load_dotenv


load_dotenv()

_db_url_env: str | None = os.getenv("DATABASE_URL")
DATABASE_URL: str = _db_url_env if _db_url_env else ""
