from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Пожалуйста, войдите в систему'

    from app.routes.web import auth, main
    from app.routes.web.event_route import events_bp

    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(events_bp)

    return app


from app.models.user import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
