import os
from dotenv import load_dotenv


load_dotenv()

CFG_DB_USER = os.environ.get("POSTGRESQL_DB_USER")
CFG_DB_PSWD = os.environ.get("POSTGRESQL_DB_PASS")
CFG_DB_HOST = os.environ.get("POSTGRESQL_DB_HOST")
CFG_DB_PORT = os.environ.get("POSTGRESQL_DB_PORT")
CFG_DB_NAME = os.environ.get("POSTGRESQL_DB_NAME")