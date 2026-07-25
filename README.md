# BiblioSmart

Platformă software modernă pentru gestionarea și digitalizarea fluxurilor de lucru din cadrul bibliotecii Colegiului Național de Informatică „Spiru Haret” Suceava.

---

## Descriere Generală

BiblioSmart digitalizează și eficientizează procesele administrative și de interacțiune din cadrul bibliotecii. Sistemul este implementat pe baza unei arhitecturi de tip MVC (Model-View-Controller) decuplată. Baza de date și logica de afaceri (Models și Controllers) sunt gestionate de serverul Flask, în timp ce interfața grafică (View) este delegată aplicației client dezvoltate în Vue.js. Această separare structurală facilitează atât managementul resurselor pentru personalul autorizat, cât și accesul rapid la informație pentru utilizatori.

## Funcționalități Principale

### Funcționalități destinate Utilizatorilor (Elevi / Cadre Didactice)
* **Catalog Digital**: Modul de căutare avansată a cărților după titlu, autor sau gen literar.
* **Sistem de Rezervări și Istoric**: Permite utilizatorilor autentificați să rezerve volume fizice online și să consulte propriul istoric de împrumuturi.
* **Clubul de Lectură**: Modul destinat interacțiunii, incluzând un forum de discuții și anunțuri privind evenimentele organizate.
* **Sistem de Evaluare**: Posibilitatea de a acorda note și de a redacta recenzii pentru materialele consultate.

### Funcționalități destinate Administratorilor (Bibliotecari)
* **Panou de Administrare**: Interfață centralizată pentru supravegherea stocului și a solicitărilor aflate în așteptare.
* **Gestiune Catalog**: Funcții complete de tip CRUD (Creare, Citire, Actualizare, Ștergere) pentru înregistrările din baza de date, incluzând suport pentru coperți și documente digitale.
* **Managementul Împrumuturilor**: Administrarea fluxului de rezervări, aprobarea acestora și actualizarea în timp real a inventarului.

## Arhitectură și Tehnologii Utilizate

Aplicația respectă arhitectura Model-View-Controller, fiind divizată astfel:

### View (Frontend)
* **Vue.js 3** - Cadru de lucru progresiv pentru dezvoltarea interfețelor de utilizator.
* **Vite** - Instrument principal de asamblare și dezvoltare rapidă.
* **Tailwind CSS** - Cadru de lucru bazat pe utilități pentru generarea de interfețe grafice adaptabile (responsive design).
* **Vue Router** - Gestiunea rutei pe partea de client.

### Model & Controller (Backend)
* **Python 3 / Flask** - Cadru de lucru stabil pentru expunerea logicii de control (Controllers).
* **SQLAlchemy** - Instrument de tip ORM (Object-Relational Mapping) pentru gestionarea structurilor de date (Models).
* **Flask-Limiter** - Implementarea politicilor de limitare a cererilor (Rate Limiting).
* **PyJWT** - Autentificare securizată utilizând token-uri web de tip JSON.
* **MySQL** - Sistemul principal de gestiune a bazelor de date relaționale.

## Structura Proiectului

Proiectul adoptă principiul separării responsabilităților (Separation of Concerns) conform modelului MVC:

```text
biblioteca-repo/
├── backend/               # Componentele Model și Controller
│   ├── app/
│   │   ├── controllers/   # Logica principală de funcționare (Controller)
│   │   ├── middlewares/   # Componente de autorizare și validare JWT
│   │   ├── models.py      # Schemele structurale ale bazei de date (Model)
│   │   └── routes/        # Definirea punctelor de acces și rutare internă
│   └── run.py             # Punctul de intrare pentru serverul Flask
│
└── frontend/              # Componenta View (Aplicația Web)
    ├── src/
    │   ├── components/    # Componente vizuale refolosibile
    │   ├── pages/         # Pagini și ecrane principale
    │   ├── router/        # Gestiunea de navigare internă a interfeței
    │   └── main.js        # Punctul de intrare pentru componenta vizuală
    └── package.json       # Gestionarea dependențelor Node.js
```

## Securitate Informatică

Platforma a fost dezvoltată cu un accent ridicat pe securitate, adoptând standardele recomandate la nivel de industrie:
* **Autentificare Stateless**: Token-urile JWT sunt stocate și transmise în siguranță exclusiv sub formă de cookie-uri HTTPOnly.
* **Protecție CSRF**: Securitate nativă asigurată de aplicarea strictă a directivei SameSite=Lax la nivel de sesiune, blocând astfel accesul scripturilor cross-domain neautorizate.
* **Mecanisme Anti-Abuz**: Punctele de autentificare beneficiază de limitarea ratei de apel (Rate Limiting) împotriva atacurilor de tip DoS (Denial of Service) și Brute-force.
* **Integritatea Datelor**: Parolele sunt protejate utilizând un algoritm robust de hashing unidirecțional (Bcrypt).

## Instrucțiuni de Configurare și Rulare Locală

### Cerințe de Sistem
* Node.js (v16 sau superior)
* Python (v3.10 sau superior)
* MySQL (v8 sau superior)

### 1. Configurarea Bazei de Date
Creați o bază de date MySQL (de exemplu, biblioteca_db) și adăugați parametrii de conectare într-un fișier .env aflat în directorul backend/:
```ini
DB_USER=root
DB_PASSWORD=parola_dorita
DB_HOST=localhost
DB_NAME=biblioteca_db
JWT_SECRET=cheie_secreta_pentru_jwt
FLASK_ENV=development
```

### 2. Lansarea Modulului Backend (Model & Controller)
```bash
cd backend
python -m venv venv
# Activare mediu virtual (Windows: venv\Scripts\activate | Unix: source venv/bin/activate)
pip install -r requirements.txt
python run.py
```

### 3. Lansarea Modulului Frontend (View)
```bash
cd frontend
npm install
npm run dev
```

Aplicația va putea fi accesată în mediul de dezvoltare la adresa: http://localhost:5173.
