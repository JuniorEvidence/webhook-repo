from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from config import Config
from flask_pymongo import PyMongo
from config import Config 


client = MongoClient(Config.MONGO_URI)


mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/github_webhooks"
    mongo.init_app(app)
    CORS(app)

    from .routes import webhook_bp
    app.register_blueprint(webhook_bp)

    return app
