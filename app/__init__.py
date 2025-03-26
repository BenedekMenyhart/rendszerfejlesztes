from apiflask import APIFlask

from app.extensions import db
from config import Config


def create_app(config_class=Config):
    # app = Flask(__name__)
    app = APIFlask(__name__, json_errors=True,
                   title="Raktar API",
                   docs_path="/swagger")
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)

    from flask_migrate import Migrate
    migrate = Migrate(app, db, render_as_batch=True)

    # Register blueprints here
    from app.blueprints import bp as main_bp
    app.register_blueprint(main_bp, url_prefix="/api")

    return app