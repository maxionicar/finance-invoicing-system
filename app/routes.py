# app/routes.py
from flask import render_template, jsonify, request
from pony.orm import db_session, select
from app.models import *
from datetime import datetime, timedelta

def register_routes(app):
    
    
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/klijenti')
    def klijenti_page():
        return render_template('klijenti.html')
    
    @app.route('/racuni')
    def racuni_page():
        return render_template('racuni.html')
    
    @app.route('/racuni/<int:id>')
    def racun_detalji_page(id):
        return render_template('racun_detalji.html', racun_id=id)
    
    @app.route('/statistika')
    def statistika_page():
        return render_template('statistika.html')
    
    @app.route('/neplaceni')
    def neplaceni_page():
        return render_template('neplaceni.html')
    
    
    @app.route('/api/klijenti', methods=['GET'])
    @db_session
    def get_klijenti():
        klijenti = select(k for k in Klijent)[:]
        return jsonify([{
            'id': k.id,
            'naziv': k.naziv,
            'oib': k.oib,
            'adresa': k.adresa,
            'kontakt': k.kontakt,
            'email': k.email,
            'broj_racuna': len(k.racuni)
        } for k in klijenti])
    
    @app.route('/api/klijenti', methods=['POST'])
    @db_session
    def create_klijent():
        data = request.json
        klijent = Klijent(
            naziv=data['naziv'],
            oib=data['oib'],
            adresa=data['adresa'],
            kontakt=data['kontakt'],
            email=data['email']
        )
        return jsonify({'id': klijent.id, 'message': 'Klijent kreiran!'}), 201
    
    @app.route('/api/klijenti/<int:id>', methods=['PUT'])
    @db_session
    def update_klijent(id):
        klijent = Klijent[id]
        data = request.json
        klijent.naziv = data.get('naziv', klijent.naziv)
        klijent.oib = data.get('oib', klijent.oib)
        klijent.adresa = data.get('adresa', klijent.adresa)
        klijent.kontakt = data.get('kontakt', klijent.kontakt)
        klijent.email = data.get('email', klijent.email)
        return jsonify({'message': 'Klijent ažuriran!'})
    
    @app.route('/api/klijenti/<int:id>', methods=['DELETE'])
    @db_session
    def delete_klijent(id):
        klijent = Klijent[id]
        if len(klijent.racuni) > 0:
            return jsonify({'error': 'Klijent ima račune!'}), 400
        klijent.delete()
        return jsonify({'message': 'Klijent obrisan!'})
    
    
    @app.route('/api/racuni', methods=['GET'])
    @db_session
    def get_racuni():
        racuni = select(r for r in Racun)[:]
        return jsonify([{
            'id': r.id,
            'broj': r.broj,
            'datum': r.datum.isoformat(),
            'klijent': r.klijent.naziv,
            'klijent_id': r.klijent.id,
            'ukupno': round(r.ukupno, 2),
            'pdv': r.pdv,
            'status': r.status
        } for r in racuni])
    
    @app.route('/api/racuni', methods=['POST'])
    @db_session
    def create_racun():
        data = request.json
        klijent = Klijent[data['klijent_id']]
        
        
        zadnji = select(r for r in Racun).order_by(lambda r: r.id)[:1]
        if zadnji:
            broj = f"R-{datetime.now().year}-{str(zadnji[-1].id + 1).zfill(3)}"
        else:
            broj = f"R-{datetime.now().year}-001"
        
        racun = Racun(
            broj=broj,
            datum=datetime.now(),
            klijent=klijent,
            pdv=data.get('pdv', 25.0),
            status='neplaćeno'
        )
        return jsonify({'id': racun.id, 'broj': racun.broj, 'message': 'Račun kreiran!'}), 201
    
    @app.route('/api/racuni/<int:id>', methods=['PUT'])
    @db_session
    def update_racun(id):
        racun = Racun[id]
        data = request.json
        if 'status' in data:
            racun.status = data['status']
        return jsonify({'message': 'Račun ažuriran!'})
    
    @app.route('/api/racuni/<int:id>', methods=['DELETE'])
    @db_session
    def delete_racun(id):
        racun = Racun[id]
        for stavka in racun.stavke:
            stavka.delete()
        racun.delete()
        return jsonify({'message': 'Račun obrisan!'})
    
    
    @app.route('/api/racuni/<int:id>/stavke', methods=['GET'])
    @db_session
    def get_stavke(id):
        racun = Racun[id]
        return jsonify([{
            'id': s.id,
            'opis': s.opis,
            'kolicina': s.kolicina,
            'cijena': s.cijena,
            'ukupno': round(s.ukupno, 2)
        } for s in racun.stavke])
    
    @app.route('/api/racuni/<int:id>/stavke', methods=['POST'])
    @db_session
    def create_stavka(id):
        racun = Racun[id]
        data = request.json
        stavka = StavkaRacuna(
            racun=racun,
            opis=data['opis'],
            kolicina=data['kolicina'],
            cijena=data['cijena']
        )
        racun.izracunaj_ukupno()
        return jsonify({'id': stavka.id, 'message': 'Stavka dodana!'}), 201
    
    @app.route('/api/stavke/<int:id>', methods=['DELETE'])
    @db_session
    def delete_stavka(id):
        stavka = StavkaRacuna[id]
        racun = stavka.racun
        stavka.delete()
        racun.izracunaj_ukupno()
        return jsonify({'message': 'Stavka obrisana!'})
    
    # ============ SPECIFIČNE FUNKCIJE - STATISTIKA ============
    @app.route('/api/statistika/dashboard', methods=['GET'])
    @db_session
    def dashboard_stats():
        return jsonify({
            'broj_racuna': select(r for r in Racun).count(),
            'ukupni_prihod': round(sum(r.ukupno for r in Racun if r.status == 'plaćeno'), 2),
            'neplaceno': round(sum(r.ukupno for r in Racun if r.status == 'neplaćeno'), 2),
            'broj_klijenata': select(k for k in Klijent).count()
        })
    
    @app.route('/api/statistika/mjesecna', methods=['GET'])
    @db_session
    def mjesecna_statistika():
        danas = datetime.now()
        rezultati = []
        for i in range(11, -1, -1):
            mjesec = danas.month - i
            godina = danas.year
            if mjesec <= 0:
                mjesec += 12
                godina -= 1
            racuni = select(r for r in Racun if r.datum.month == mjesec 
                           and r.datum.year == godina and r.status == 'plaćeno')
            rezultati.append({
                'mjesec': f"{mjesec:02d}/{godina}",
                'iznos': round(sum(r.ukupno for r in racuni), 2)
            })
        return jsonify({
            'mjeseci': [r['mjesec'] for r in rezultati],
            'iznosi': [r['iznos'] for r in rezultati]
        })
    
    @app.route('/api/statistika/status', methods=['GET'])
    @db_session
    def status_statistika():
        return jsonify({
            'placeno': round(sum(r.ukupno for r in Racun if r.status == 'plaćeno'), 2),
            'neplaceno': round(sum(r.ukupno for r in Racun if r.status == 'neplaćeno'), 2)
        })
    
    @app.route('/api/statistika/top_klijenti', methods=['GET'])
    @db_session
    def top_klijenti():
        podaci = []
        for k in select(k for k in Klijent)[:]:
            ukupno = sum(r.ukupno for r in k.racuni if r.status == 'plaćeno')
            podaci.append({'naziv': k.naziv, 'ukupno': round(ukupno, 2)})
        podaci.sort(key=lambda x: x['ukupno'], reverse=True)
        top5 = podaci[:5]
        return jsonify({
            'klijenti': [p['naziv'] for p in top5],
            'iznosi': [p['ukupno'] for p in top5]
        })
    
    @app.route('/api/statistika/neplaceni', methods=['GET'])
    @db_session
    def neplaceni_racuni():
        racuni = select(r for r in Racun if r.status == 'neplaćeno')[:]
        return jsonify([{
            'id': r.id,
            'broj': r.broj,
            'datum': r.datum.isoformat(),
            'klijent': r.klijent.naziv,
            'ukupno': round(r.ukupno, 2)
        } for r in racuni])
    
    @app.route('/api/seed', methods=['POST'])
    def seed_database():
        from app.seed import seed
        seed()
        return jsonify({'message': 'Test podaci dodani!'})