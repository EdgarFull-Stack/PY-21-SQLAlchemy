from sqlalchemy import Column, create_engine, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy import func
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
# Funkcija, kuri patikrina, ar mokinys jau yra duomenų bazėje
def ar_mokinys_yra(vardas, pavarde):
    return session.query(Mokinys).filter_by(vardas=vardas, pavarde=pavarde).first() is not None

def ar_mokytojas_yra(vardas, pavarde):
    mokytojai = session.query(Mokytojas).all()
    for row in mokytojai:
        if row.vardas == vardas and row.pavarde == pavarde:
            return True

# Pridedame mokinius, jei jų dar nėra
mokiniai = [
    ("Jonas", "Jonaitis", 5),
    ("Petras", "Petraitis", 6),
    ("Asta", "Astaitė", 7),
    ("Edgar", "Lip", 10),
    ("Jack","Jack",10)
]
#
for vardas, pavarde, klase in mokiniai:
    if not ar_mokinys_yra(vardas, pavarde):
        session.add(Mokinys(vardas=vardas, pavarde=pavarde, klase=klase))

# # Pridedame mokytojus
# mokytojai = [
#     Mokytojas(vardas="Rasa", pavarde="Rasaitė", dalykas="Matematika"),
#     Mokytojas(vardas="Tomas", pavarde="Tomaitis", dalykas="Fizika")
# ]
#
# session.add_all(mokytojai)

# Išsaugome pakeitimus
session.commit()

# Funkcija mokinių sąrašo išvedimui
def spausdinti_mokinius():
    mokiniai = session.query(Mokinys).all()
    for mokinys in mokiniai:
        print(f"{mokinys.vardas} {mokinys.pavarde}, klasė: {mokinys.klase}")

# Funkcija mokytojų sąrašo išvedimui
def spausdinti_mokytojus():
    mokytojai = session.query(Mokytojas).all()
    for mokytojas in mokytojai:
        print(f"{mokytojas.vardas} {mokytojas.pavarde}, dėsto: {mokytojas.dalykas}")

# Testuojame funkcijas
print("Mokiniai:")
spausdinti_mokinius()

print("\nMokytojai:")
spausdinti_mokytojus()
print('-'*40)
# Funkcija istrina mokini
def istrinti_mokini(id):
    mokinys = session.query(Mokinys).filter_by(id=id).first()
    if mokinys:
        session.delete(mokinys)
        session.commit()
        print(f'Mokinys {id} istrintas')
    else:
        print(f'Mokinys su {id} ID nerastas')
# Funkcija istrina mokytoja
def istrinti_mokytoja(id):
    mokytojas = session.query(Mokytojas).filter_by(id=id).first()
    if mokytojas:
        session.delete(mokytojas)
        session.commit()
        print(f'Mokytojas {id} istrintas')
    else:
        print(f'Mokytojas su {id} ID nerastas')
#  Funkcija trinti baigusius mokykla
def istrinti_baigusius():
    mokiniai = session.query(Mokinys).filter_by(klase = 12).all()
    if mokiniai:
        for mokinys in mokiniai:
            session.delete(mokinys)
            session.commit()
        print('Visi kas baige 12 klasiu istrinti')
    else:
        print('Nera kas baiges 12 klase')

istrinti_baigusius()
istrinti_mokytoja(1)
istrinti_mokini(1)
print('-'*40)
#  Funckija filtruota mokini pagal varda
def filtruoti_mokini_varda(vardas):
    try:
        mokinys = session.query(Mokinys).filter_by(vardas=vardas).one()
        print(f'Rastas mokinys: {mokinys.vardas} {mokinys.pavarde} {mokinys.id}')
    except NoResultFound:
        print('Tokio mokinio nera')
    except MultipleResultsFound:
        print('Rasta daugiau nei vienas mokinys su tokiu vardu')
#  Funckija filtruoti mokini pagal pavarde "P" raide pradzioje
def filtruoti_pagal_pavarde():
    mokiniai = session.query(Mokinys).filter(Mokinys.pavarde.ilike('P%')).all()
    if mokiniai:
        for mokinys in mokiniai :
            print(f'Rastas mokinys: {mokinys.vardas} {mokinys.pavarde}')
    else:
        print('Mokiniu su pavarde is P nerasta')
filtruoti_mokini_varda('Jonas')
filtruoti_pagal_pavarde()
print('-'*40)

#  Funckija filtruota mokytoja pagal varda "S" raide pradzioje
def filtruoti_mokytoja_pagal_varda():
    mokytojai = session.query(Mokytojas).filter(Mokytojas.vardas.ilike('%s'))
    if mokytojai:
        for mokytojas in mokytojai :
            print(f'Rastas mokytojas: {mokytojas.vardas} {mokytojas.pavarde}')
    else:
        print('Mokytojo su pavardes pabaiga s nerasta')
filtruoti_mokytoja_pagal_varda()

print('-'*40)
# Funkcija kuri isveda mokinius pagal klase (didejancia tvarka)
def mokiniai_pagal_klase():
    mokiniai = session.query(Mokinys).order_by(Mokinys.klase).all()
    for mokinys in mokiniai:
        print(f'{mokinys.vardas} {mokinys.pavarde} klase: {mokinys.klase}')
mokiniai_pagal_klase()
print('-'*40)
# Funkcija kuri skaiciuoja kiek yra mokiniu kiekvienoje klaseje
def mokiniu_skaicius_klaseje():
    suma = session.query(Mokinys.klase, func.count(Mokinys.id)).group_by(Mokinys.klase).all()
    for klase, kiekis in suma:
        print(f'Klase: {klase}, mokiniu skaicius: {kiekis}')
mokiniu_skaicius_klaseje()
# Funkcija koks mokiniu vidurkis klaseje
def vidutinis_mokiniu_skaicius():
    bendras_mokiniu_skaicius = session.query(Mokinys).count()
    skirtingu_klasiu_skaicius = session.query(Mokinys.klase).distinct().count()
    if skirtingu_klasiu_skaicius > 0:
        vidurkis = bendras_mokiniu_skaicius / skirtingu_klasiu_skaicius
    else:
        vidurkis = 0
    print(f'Vidutinis mokiniu skaicius klaseje: {vidurkis:.2f}')
vidutinis_mokiniu_skaicius()