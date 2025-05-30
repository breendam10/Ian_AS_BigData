from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Instâncias das extensões
db = SQLAlchemy()
migrate = Migrate()