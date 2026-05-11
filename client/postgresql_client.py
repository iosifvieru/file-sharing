from os import getenv
from dotenv import load_dotenv
from psycopg_pool import ConnectionPool

load_dotenv()

POSTGRES_USER = getenv("POSTGRES_USER", "admin")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD", "password")
POSTGRES_DB = getenv("POSTGRES_DB", "filesharing")
POSTGRES_HOST = getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = getenv("POSTGRES_PORT", "5432")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

pool = ConnectionPool(conninfo=DATABASE_URL, kwargs={"sslmode": "require"})

def create_file_record(unique_key, file_name, file_size_bytes):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO file_informations (
                    unique_key,
                    file_name,
                    file_size_bytes
                )
                VALUES (%s, %s, %s)
                RETURNING id;
                """,
                (unique_key, file_name, file_size_bytes),
            )
            return cur.fetchone()[0]
        
def increment_download_number(unique_key: str, file_name: str):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE file_informations
                SET download_number = download_number + 1
                WHERE unique_key = %s
                  AND file_name = %s
                RETURNING download_number;
                """,
                (unique_key, file_name),
            )

            result = cur.fetchone()

            if result is None:
                return None
            
            conn.commit()

            return result[0]  # updated download count

def get_files_by_unique_key(unique_key: str):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    file_name,
                    file_size_bytes,
                    download_number,
                    uploaded_at
                FROM file_informations
                WHERE unique_key = %s;
                """,
                (unique_key,),
            )

            rows = cur.fetchall()

            return [
                {
                    "file_name": row[0],
                    "file_size_bytes": row[1],
                    "download_number": row[2],
                    "uploaded_at": row[3],
                }
                for row in rows
            ]
