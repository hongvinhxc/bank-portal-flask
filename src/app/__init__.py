from flask import Flask
from flasgger import Swagger
from flask_cors import CORS
from .controllers.account import api as accounts_module
from .controllers.auth import api as auth_module
from .utils.auth import createDefautlUser

def create_app():
  app = Flask(__name__)
  CORS(app)
  swagger = Swagger(app)

  createDefautlUser()

  app.register_blueprint(accounts_module)
  app.register_blueprint(auth_module)

  return app