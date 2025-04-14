import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "my secret key"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
        or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

def load_private_key():
    path = os.path.abspath(os.path.dirname(__file__))
    key_path = os.path.join(path, ".ssh", "private-key.pem")
    with open(key_path, 'r') as f:
        return f.read()