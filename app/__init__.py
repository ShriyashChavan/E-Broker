from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)

    login_manager.login_view = 'auth.login'

    from app import models

    from app.routes.auth import auth_bp
    from app.routes.properties import properties_bp
    from app.routes.appointments import appointments_bp
    from app.routes.feedback import feedback_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(properties_bp)
    app.register_blueprint(appointments_bp)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(admin_bp)

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import Tenant, Landlord, Admin
    # user_id format: "type:id" to avoid collisions between tables
    if ':' in user_id:
        user_type, user_id_num = user_id.split(':', 1)
        user_id_num = int(user_id_num)
        
        if user_type == 'tenant':
            return Tenant.query.get(user_id_num)
        elif user_type == 'landlord':
            return Landlord.query.get(user_id_num)
        elif user_type == 'admin':
            return Admin.query.get(user_id_num)
    else:
        # Fallback for old sessions - try to load from each model
        user = Tenant.query.get(int(user_id))
        if user:
            return user
        user = Landlord.query.get(int(user_id))
        if user:
            return user
        user = Admin.query.get(int(user_id))
        return user