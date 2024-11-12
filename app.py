import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow

# Cargar variables de entorno
load_dotenv()

# Inicializar la aplicación
app = Flask(__name__)

# Configuración de la aplicación con variables de entorno
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')  # Cambia esto a 'DATABASE_URI' para que coincida
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')  # Usamos 'JWT_SECRET_KEY' como token de autenticación

# Inicializar extensiones
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
ma = Marshmallow(app)

# Importar modelos para evitar problemas de importación circular
from models import Producto, User  # Cambia los nombres según los modelos de perfumería

# Registrar los blueprints
from views import register_bp
register_bp(app)

if __name__ == "__main__":
    app.run(debug=True)
