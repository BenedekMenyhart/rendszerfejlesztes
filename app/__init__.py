from flask import Flask

from config import Config


def create_app(config_class=Config):
    # app = Flask(__name__)
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)

    from flask_migrate import Migrate
    migrate = Migrate(app, db, render_as_batch=True)

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app