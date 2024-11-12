from .auth_views import auth_blueprint as auth_bp
from .productos_view import productos_blueprint as productos_bp

def register_bp(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(productos_bp)
