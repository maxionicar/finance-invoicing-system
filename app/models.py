# app/models.py
from pony.orm import *
from datetime import datetime


db = Database()

class Klijent(db.Entity):

    id = PrimaryKey(int, auto=True)
    naziv = Required(str, 100)
    oib = Required(str, 11, unique=True)
    adresa = Required(str, 200)
    kontakt = Required(str, 100)
    email = Required(str, 100)
    racuni = Set('Racun')

class Racun(db.Entity):

    id = PrimaryKey(int, auto=True)
    broj = Required(str, 20, unique=True)
    datum = Required(datetime)
    klijent = Required(Klijent)
    ukupno = Required(float, default=0.0)
    pdv = Required(float, default=25.0)
    status = Required(str, default='neplaćeno')
    stavke = Set('StavkaRacuna')

    def izracunaj_ukupno(self):

        total = sum(stavka.ukupno for stavka in self.stavke)
        self.ukupno = total * (1 + self.pdv / 100)
        return self.ukupno

class StavkaRacuna(db.Entity):

    id = PrimaryKey(int, auto=True)
    racun = Required(Racun)
    opis = Required(str, 200)
    kolicina = Required(int, default=1)
    cijena = Required(float)
    ukupno = Optional(float, default=0.0)

    def before_insert(self):

        self.ukupno = self.kolicina * self.cijena


db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)

print(" Baza podataka je spremna")