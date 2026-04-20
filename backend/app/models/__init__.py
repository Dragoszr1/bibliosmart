"""Database models for the library application"""

# Import db from the database module
from app.database import db

class Carti(db.Model):
    """Books table model - matches existing 'carti' table"""
    __tablename__ = 'carti'

    carte_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titlu = db.Column(db.String(50), nullable=False)
    autor = db.Column(db.String(50), nullable=False)
    ISBN = db.Column(db.String(13), nullable=False, unique=True)
    stoc_total = db.Column(db.Integer)
    stoc_disponibil = db.Column(db.Integer)
    imprumutat = db.Column(db.Boolean)
    gen = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Carti {self.titlu}>'

class Users(db.Model):
    """Users table model - matches existing 'users' table"""
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum('user', 'bibliotecar', name='user_role'), nullable=False, default='user')
    telefon = db.Column(db.String(50), nullable=True, unique=True)
    description = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Users {self.username}>'

class CartiCitite(db.Model):
    """Books read table model - matches existing 'carti_citite' table"""
    __tablename__ = 'carti_citite'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    carte_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<CartiCitite user:{self.user_id} carte:{self.carte_id}>'

class Recenzii(db.Model):
    """Reviews table model - matches existing 'recenzii' table"""
    __tablename__ = 'recenzii'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    carte_id = db.Column(db.Integer, nullable=False)
    nota = db.Column(db.Integer, nullable=False)
    comentariu = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Recenzii user:{self.user_id} carte:{self.carte_id} nota:{self.nota}>'

class Anunturi(db.Model):
    """Announcements table model"""
    __tablename__ = 'anunturi'

    anunt_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titlu = db.Column(db.String(255), nullable=False)
    anunt = db.Column(db.Text, nullable=True)
    data_publicare = db.Column(db.DateTime, nullable=False, default=db.func.now())
    aprecieri = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Anunturi {self.anunt_id}: {self.titlu}>'

class AnunturiAprecieri(db.Model):
    """Announcement likes tracking table"""
    __tablename__ = 'anunturi_aprecieri'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    anunt_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)


class CereriCarti(db.Model):
    """Book borrow requests table"""
    __tablename__ = 'cereri_carti'

    cerere_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    carte_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum('pending', 'approved', 'rejected', name='cerere_status'), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f'<CereriCarti {self.cerere_id}: user={self.user_id} carte={self.carte_id} status={self.status}>'

    def __repr__(self):
        return f'<AnunturiAprecieri anunt:{self.anunt_id} user:{self.user_id}>'
