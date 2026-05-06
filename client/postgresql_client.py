from os import getenv
from psycopg_pool import ConnectionPool

POSTGRES_USER = getenv("POSTGRES_USER", "admin")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD", "password")
POSTGRES_DB = getenv("POSTGRES_DB", "filesharing")
POSTGRES_HOST = getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = getenv("POSTGRES_PORT", "5432")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

pool = ConnectionPool(conninfo=DATABASE_URL)

