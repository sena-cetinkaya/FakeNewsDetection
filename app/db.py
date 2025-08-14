from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

env_path = os.getenv("ENV_PATH", "config/dev/.env.dev")
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.create_all(engine)
    