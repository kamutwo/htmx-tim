import os
from sqlmodel import create_engine, SQLModel
from dotenv import load_dotenv


load_dotenv()
engine = create_engine(os.getenv("DB_CONN_URL"))


def init_db():
    SQLModel.metadata.create_all(engine)
