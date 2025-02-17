from sqlalchemy import Column, create_engine, Integer, String
from sqlalchemy.orm import declarative_base
# Task 1
engine = create_engine("sqlite:///mokykla.db")
Base = declarative_base()

class Mokinys(Base):
    __tablename__ = 'mokiniai'
    id = Column(Integer, primary_key=True)
    vardas = Column(String)
    pavarde = Column(String)
    klase = Column(Integer)

class Mokytojas(Base):
    __tablename__ = 'mokytojai'
    id = Column(Integer, primary_key=True)
    vardas = Column(String)
    pavarde = Column(String)
    dalykas = Column(String)

Base.metadata.create_all(engine)

# Task 2
# 1
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()
# 2
def prideti_mokini(vardas, pavarde, klase):
    egzistuojantis = session.query(Mokinys).filter_by(vardas=vardas, pavarde=pavarde, klase=klase).first()
    if not egzistuojantis:
        naujas_mokinys = Mokinys(vardas=vardas, pavarde=pavarde, klase=klase)
        session.add(naujas_mokinys)
        session.commit()
        print(f'Mokinys {vardas} {pavarde} (klase: {klase}) pridėtas.')
    else:
        print(f'Mokinys {vardas} {pavarde} jau egzistuoja duomenų bazeje.')

# 3
prideti_mokini("Jonas", "Jonaitis", 9)
prideti_mokini("Edgar", "Lip", 10)
prideti_mokini("Tomas", "Tomaitis", 11)
prideti_mokini("Jonas", "Jonaitis", 9)
# mokytojas1 = Mokytojas(id = 777, vardas = 'Darius',pavarde = 'Das', dalykas = 'Python')
# mokytojas2 = Mokytojas(id = 767, vardas = 'Dar',pavarde = 'Das', dalykas = 'SQL')
# session.add(mokytojas1)
# session.add(mokytojas2)
# session.commit()
#4
visi_mokiniai = session.query(Mokinys).all()
for mokiniai in visi_mokiniai:
    print(f'Id: {mokiniai.id}, Vardas: {mokiniai.vardas}, Pavarde: {mokiniai.pavarde}, Klase: {mokiniai.klase}')

visi_mokytojai = session.query(Mokytojas).all()
for mokytojas in visi_mokytojai:
    print(f'Id: {mokytojas.id}, Vardas: {mokytojas.vardas}, Pavarde: {mokytojas.pavarde}, Dalykas: {mokytojas.dalykas}')