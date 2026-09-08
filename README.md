# Naziv projekta:
Sustav za upravljanje računima i financijama


# Opis projekta:
Web aplikacija za upravljanje poslovnim računima

Mogućnosti aplikacije:  

- Upravljanje klijentima 
- Upravljanje računima 
- Upravljanje stavkama računa
- Praćenje statusa računa (plaćeno/neplaćeno)
- Financijsku statistiku s grafikonima
- Pregled neplaćenih računa


# Korištene tehnologije:
- Python 3.9 -- Programski jezik
- Flask -- Web framework
- PonyORM -- ORM za bazu podataka
- SQLite -- Baza podataka
- Bootstrap 5 -- CSS framework
- Chart.js -- Grafikoni
- Docker -- Kontejnerizacija

# Pokretanje aplikacije

Postoji više opcija pokretanja:  

-Lokalno  

    pip install -r requirements.txt
    python app.py  

-Docker  

    docker build -t finance-app .
    docker run -p 5000:5000 finance-app  

-Docker Compose  

    docker-compose up --build


# Testni podaci

Nakon pokretanja, na dashboardu kliknite "Dodaj test podatke" za dodavanje:
- 3 klijenta
- 4 računa
- Stavke na račune

# Struktura projekta

finance-invoicing-system/  

    app/ #Backend  

        init.py  

        models.py #Baza podataka  

        routes.py #API rute  
        
        seed.py #Test podaci
    templates/ #HTML predlošci
        base.html #osnovni preložak
        index.html #Dashboard
        klijenti.html #Klijenti
        racuni.html #Računi
        racun_detalji.html #Detalji računa
        statistika.html #Grafikoni
        neplaceni.html #Neplaćeni računi
    app.py #Glavna aplikacija
    requirements.txt #Python paketi
    Dockerfile #Docker konfiguracija
    docker-compose.yml #Docker kompozicija
    README.md #Dokumentacija

# API Endpointovi

## Klijenti  

-GET	    Dohvat svih klijenata  

-POST    Dodavanje klijenta  

-PUT	    Ažuriranje klijenta  

-DELETE	Brisanje klijenta  


## Računi
-GET     Dohvat stavki  

-POST    Dodavanje stavke  

-DELETE  Brisanje stavke  


## Statistika
-GET     Podaci za dashbboard  

-GET     Mjesecni prihod(Dijagram)  

-GET     Omjer plaćenih/neplaćenih(Dijagram)  

-GET     Top 5 klijenata(Dijagram)  

-GET     Lista neplaćenih  


# Grafikoni
-svi grafikoni se prikazuju na stranici /statistika

## Prvi grafikon:
Mjesečni prihodi -- bar chart -- prihodi po mjesecima

## Drugi grafikon:
Omjer plaćenih/neplaćenih -- pie chart -- Uio plaćenih i neplaćenih

## Treći dijagram:
Top 5 klijenata -- Bar chart -- 5 klijenata s najvećim prihodom

# Use Case Dijagram

## Akter:
Radnik - Upravlja svim podacima u sustavu

# Funkcionalnost:
Upravljanje klijentima -- Dodavanje, uređivanje, pregled i brisanje klijenata  

Upravljanje računima -- Kreiranje, pregled, uređivanje i brisanje računa   

Pregled statistike --  Prikaz grafikona: mjesečni prihodi, omjer plaćenih/neplaćenih, top 5 klijenata  

Pregled neplaćenig računa -- Lista svih neplaćenih računa s ukupnim iznosom  

Pretraga računa --  Pretraga računa po broju ili klijentu  
