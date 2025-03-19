from flask import Flask
from app import create_app
from config import Config
if __name__ == '__main__':
    create_app(config_class=Config).run("localhost", 8080)
