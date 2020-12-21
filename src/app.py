from flask import Flask
from flasgger import Swagger
from flask_cors import CORS
from controllers.account import api as accounts_module

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)

app.register_blueprint(accounts_module)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)