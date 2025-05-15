from apiflask import APIFlask
from flask_login import LoginManager
from app.extensions import db
from config import Config
from app.models.user import User


def create_app(config_class=Config):
    app = APIFlask(__name__, json_errors=True,
                   title="Raktar API",
                   docs_path="/swagger")
    app.config.from_object(config_class)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    login_manager.login_view = 'user_index'

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    from flask_migrate import Migrate
    migrate = Migrate(app, db, render_as_batch=True)

    # Register blueprints here
    from app.blueprints import bp as main_bp
    app.register_blueprint(main_bp, url_prefix="/api")

    return app