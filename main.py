# Example
from sqlalchemy import Column, create_engine, Integer, String, Float
from sqlalchemy.orm import declarative_base

engine = create_engine("sqlite:///projektai.db")
Base = declarative_base()

class Projektas(Base):
    __tablename__ = 'projektai'
    id = Column(Integer, primary_key=True)
    pavadinimas = Column(String)
    kaina = Column(Float)

Base.metadata.create_all(engine)
# Example
