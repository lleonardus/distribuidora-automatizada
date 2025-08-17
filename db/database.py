import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

DATABASE = os.getenv(key="DATABASE", default="sqlite:///distribuidora.db")

engine = create_engine(DATABASE, echo=True)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass
