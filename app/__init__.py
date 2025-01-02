from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv()


def create_app(db_instance):

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URI", "postgresql://user:password@db:5432/robot_service"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db_instance.init_app(app)
    Migrate(app, db_instance)

    return app


db = SQLAlchemy()
