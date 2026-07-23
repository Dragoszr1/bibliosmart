"""Modele SQLAlchemy pentru baza de date a bibliotecii."""

# Importăm obiectul db din modulul database
from app.database import db

class Carti(db.Model):
    """Modelul tabelei carti din baza de date."""
    __tablename__ = 'carti'

    carte_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titlu = db.Column(db.String(50), nullable=False)
    autor = db.Column(db.String(50), nullable=False)
    ISBN = db.Column(db.String(13), nullable=False, unique=True)
    stoc_total = db.Column(db.Integer)
    stoc_disponibil = db.Column(db.Integer)
    imprumutat = db.Column(db.Boolean)
    gen = db.Column(db.String(255), nullable=False)
    pozitie = db.Column(db.String(100), nullable=True)
    cod = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<Carti {self.titlu}>'

class Users(db.Model):
    """Modelul tabelei users din baza de date."""
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum('user', 'bibliotecar', name='user_role'), nullable=False, default='user')
    telefon = db.Column(db.String(50), nullable=True, unique=True)
    description = db.Column(db.String(255), nullable=True)
    club = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Users {self.username}>'

class CartiCitite(db.Model):
    """Modelul tabelei carti_citite — cărți citite/returnate per utilizator."""
    __tablename__ = 'carti_citite'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    carte_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<CartiCitite user:{self.user_id} carte:{self.carte_id}>'

class Recenzii(db.Model):
    """Modelul tabelei recenzii — notă și comentariu per carte per utilizator."""
    __tablename__ = 'recenzii'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    carte_id = db.Column(db.Integer, nullable=False)
    nota = db.Column(db.Integer, nullable=False)
    comentariu = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Recenzii user:{self.user_id} carte:{self.carte_id} nota:{self.nota}>'

class Anunturi(db.Model):
    """Modelul tabelei anunturi — anunțuri publicate de bibliotecar."""
    __tablename__ = 'anunturi'

    anunt_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titlu = db.Column(db.String(255), nullable=False)
    anunt = db.Column(db.Text, nullable=True)
    data_publicare = db.Column(db.DateTime, nullable=False, default=db.func.now())
    aprecieri = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Anunturi {self.anunt_id}: {self.titlu}>'

class AnunturiAprecieri(db.Model):
    """Modelul tabelei anunturi_aprecieri — aprecierile utilizatorilor la anunțuri."""
    __tablename__ = 'anunturi_aprecieri'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    anunt_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<AnunturiAprecieri anunt:{self.anunt_id} user:{self.user_id}>'


class CereriCarti(db.Model):
    """Modelul tabelei cereri_carti — cereri de împrumut fizic."""
    __tablename__ = 'cereri_carti'

    cerere_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    carte_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum('pending', 'approved', 'rejected', 'ridicat', 'returnat', name='cerere_status'), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f'<CereriCarti {self.cerere_id}: user={self.user_id} carte={self.carte_id} status={self.status}>'


class ImprumuturiActive(db.Model):
    """Modelul tabelei imprumuturi_active — împrumuturi aprobate și active."""
    __tablename__ = 'imprumuturi_active'

    imprumut_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    carte_id = db.Column(db.Integer, db.ForeignKey('carti.carte_id', ondelete='CASCADE'), nullable=False)
    data_imprumut = db.Column(db.DateTime, nullable=False, default=db.func.now())
    data_scadenta = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<ImprumuturiActive {self.imprumut_id}: user={self.user_id} carte={self.carte_id} scadenta={self.data_scadenta}>'


class ClubThreads(db.Model):
    """Modelul tabelei club_threads — thread-urile din clubul de lectură."""
    __tablename__ = 'club_threads'

    thread_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titlu = db.Column(db.String(255), nullable=False)
    continut = db.Column(db.Text, nullable=False)
    creat_de = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    creat_la = db.Column(db.DateTime, nullable=False, default=db.func.now())
    aprobat = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<ClubThreads {self.thread_id}: {self.titlu}>'

class ThreadComments(db.Model):
    """Modelul tabelei thread_comments — comentariile la thread-uri."""
    __tablename__ = 'thread_comments'

    comentariu_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('club_threads.thread_id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    continut = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Integer, default=0)
    creat_la = db.Column(db.DateTime, nullable=False, default=db.func.now())

    def __repr__(self):
        return f'<ThreadComments {self.comentariu_id} la thread {self.thread_id}>'

class ThreadSubcomments(db.Model):
    """Modelul tabelei thread_subcomments — subcomentariile la comentariile de thread."""
    __tablename__ = 'thread_subcomments'

    subcomentariu_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comentariu_id = db.Column(db.Integer, db.ForeignKey('thread_comments.comentariu_id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    continut = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Integer, default=0)
    creat_la = db.Column(db.DateTime, nullable=False, default=db.func.now())

    def __repr__(self):
        return f'<ThreadSubcomments {self.subcomentariu_id} la comentariul {self.comentariu_id}>'

class PasswordResetTokens(db.Model):
    """Modelul tabelei password_reset_tokens — tokenuri pentru resetarea parolei."""
    __tablename__ = 'password_reset_tokens'

    token = db.Column(db.String(255), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<PasswordResetTokens {self.token} pentru user_id {self.user_id}>'
