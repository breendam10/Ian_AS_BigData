from flask import Flask
from config import config
from .extensions import db, migrate
from .routes import bp as matriculas_bp


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Inicializa extensões
    db.init_app(app)
    migrate.init_app(app, db)

    # Cria tabelas automaticamente em dev
    if app.config.get('DEBUG'):
        with app.app_context():
            db.create_all()

    # Registra blueprint de matrículas
    app.register_blueprint(matriculas_bp, url_prefix='/api/matriculas')

    return app