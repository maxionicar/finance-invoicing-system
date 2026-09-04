# app/seed.py
from pony.orm import db_session
from models import *
from datetime import datetime, timedelta

def seed():
    
    with db_session:
        
        if select(k for k in Klijent).count() > 0:
            print("ℹ Baza već ima podataka")
            return
        
        print(" Dodajem testne podatke")
        
        
        k1 = Klijent(
            naziv="IT Solutions d.o.o.",
            oib="12345678901",
            adresa="Zagreb, Ilica 1",
            kontakt="Ana Horvat",
            email="ana@itsolutions.hr"
        )
        
        k2 = Klijent(
            naziv="Digital Marketing Ltd.",
            oib="98765432109",
            adresa="Split, Poljička 5",
            kontakt="Marko Kovač",
            email="marko@digital.hr"
        )
        
        k3 = Klijent(
            naziv="Gradska knjižnica",
            oib="45678901234",
            adresa="Rijeka, Trg 1",
            kontakt="Iva Novosel",
            email="iva@knjiznica.hr"
        )

        
        r1 = Racun(
            broj="R-2026-001",
            datum=datetime.now() - timedelta(days=30),
            klijent=k1,
            pdv=25.0,
            status="plaćeno"
        )
        
        r2 = Racun(
            broj="R-2026-002",
            datum=datetime.now() - timedelta(days=15),
            klijent=k2,
            pdv=25.0,
            status="neplaćeno"
        )
        
        r3 = Racun(
            broj="R-2026-003",
            datum=datetime.now() - timedelta(days=5),
            klijent=k3,
            pdv=25.0,
            status="plaćeno"
        )
        
        r4 = Racun(
            broj="R-2026-004",
            datum=datetime.now() - timedelta(days=45),
            klijent=k1,
            pdv=25.0,
            status="neplaćeno"
        )

        
        StavkaRacuna(racun=r1, opis="Web hosting - godišnji", kolicina=1, cijena=1000.00)
        StavkaRacuna(racun=r1, opis="Konzultacije - 5h", kolicina=5, cijena=50.00)
        
        StavkaRacuna(racun=r2, opis="SEO optimizacija", kolicina=1, cijena=750.00)
        
        StavkaRacuna(racun=r3, opis="Softver za knjižnicu", kolicina=1, cijena=2000.00)
        StavkaRacuna(racun=r3, opis="Instalacija", kolicina=1, cijena=150.00)
        
        StavkaRacuna(racun=r4, opis="Licence - 3 kom", kolicina=3, cijena=150.00)

        
        for racun in [r1, r2, r3, r4]:
            racun.izracunaj_ukupno()

        
        