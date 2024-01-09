from enum import Enum, auto
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Estado(Enum):
    ACTIVO = auto()
    INACTIVO = auto()
    PENDIENTE = auto()

class TipoConsulta(Enum):
    GENERAL = auto()
    ESPECIALIZADA = auto()

class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    consultas = db.relationship('Consulta', backref='hospital', lazy=True)
    pacientes = db.relationship('Paciente', backref='hospital', lazy=True)

class Consulta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cantPacientes = db.Column(db.Integer, nullable=False)
    nombreEspecialista = db.Column(db.String(100), nullable=False)
    tipoConsulta = db.Column(db.Enum(TipoConsulta), nullable=False)
    estado = db.Column(db.Enum(Estado), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    noHistoriaClinica = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)

    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)

    def __init__(self, **kwargs):
        super(Paciente, self).__init__(**kwargs)
        if self.edad <= 15:
            self.tipo = 'ninno'
        elif 16 <= self.edad <= 40:
            self.tipo = 'joven'
        else:
            self.tipo = 'anciano'

    __mapper_args__ = {
        'polymorphic_identity':'paciente',
        'polymorphic_on':tipo
    }

class PAnciano(Paciente):
    tieneDieta = db.Column(db.Boolean)

    __mapper_args__ = {
        'polymorphic_identity':'anciano',
    }

class PJoven(Paciente):
    fumador = db.Column(db.Boolean)

    __mapper_args__ = {
        'polymorphic_identity':'joven',
    }

class PNinno(Paciente):
    relacionPesoEstatura = db.Column(db.Integer)

    __mapper_args__ = {
        'polymorphic_identity':'ninno',
    }
