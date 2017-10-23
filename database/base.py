from .conn import engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine, expire_on_commit=False)
