from flask import Blueprint, request, jsonify, abort
from sqlalchemy.exc import IntegrityError
from .extensions import db
from .models import Matricula

bp = Blueprint('matriculas', __name__)

@bp.route('/', methods=['POST'])
def criar_matricula():
    data = request.get_json() or {}
    nome = data.get('nome')
    email = data.get('email')
    curso = data.get('curso')

    if not nome or not email or not curso:
        return jsonify({'error': 'Campos nome, email e curso são obrigatórios'}), 400

    # Gera matrícula única
    codigo = Matricula.gerar_codigo()

    matricula = Matricula(
        matricula=codigo,
        nome=nome,
        email=email,
        curso=curso
    )
    db.session.add(matricula)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Email já utilizado em outro cadastro'}), 400
    except Exception as e:
        db.session.rollback()
        abort(500, description=str(e))

    return jsonify({'matricula': codigo}), 201

@bp.route('/<string:matricula_id>', methods=['GET'])
def obter_matricula(matricula_id):
    matricula = Matricula.query.get(matricula_id)
    if not matricula:
        return jsonify({'error': 'Matrícula não encontrada'}), 404

    return jsonify({
        'matricula': matricula.matricula,
        'nome': matricula.nome,
        'email': matricula.email,
        'curso': matricula.curso
    })

@bp.route('/', methods=['GET'])
def listar_matriculas():
    """
    Retorna todas as matrículas cadastradas
    """
    matriculas = Matricula.query.all()
    resultado = [{
        'matricula': m.matricula,
        'nome': m.nome,
        'email': m.email,
        'curso': m.curso
    } for m in matriculas]
    return jsonify(resultado)