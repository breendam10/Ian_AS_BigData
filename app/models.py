import random
from datetime import datetime
from .extensions import db

class Matricula(db.Model):
    __tablename__ = 'matriculas'

    matricula = db.Column(db.String(12), primary_key=True, unique=True)
    nome = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    curso = db.Column(db.String(64), nullable=False)

    @staticmethod
    def gerar_codigo():
        """
        Gera um código de matrícula no formato:
        YYYYSS######
        - YYYY: ano atual
        - SS: semestre (01 ou 02)
        - ######: número aleatório de 6 dígitos
        """
        ano = datetime.now().year
        semestre = 1 if datetime.now().month <= 6 else 2
        while True:
            sufixo = f"{random.randint(0, 999999):06d}"
            codigo = f"{ano}{semestre:02d}{sufixo}"
            if not Matricula.query.get(codigo):
                return codigo