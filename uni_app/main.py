import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    
    # Creating the flask app object - this is the core of our app!
    app = Flask(__name__)

    app.config.from_object("config.app_config")

    db.init_app(app)

    # Then we can register our routes!
    from controllers import registerable_controllers
    for controller in registerable_controllers:
        app.register_blueprint(controller)
    
    return app