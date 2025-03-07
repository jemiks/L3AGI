from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from config import Config

engine = create_engine(Config.DB_URI, echo=Config.NODE_ENV == "local")
Base = declarative_base()
