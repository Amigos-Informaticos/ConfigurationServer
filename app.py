from flask import Flask

from src.Configuration.JSONHandler import JSONHandler
from src.Configuration.Paths import api_configuration_path
from src.routes.ClientConfiguration import client_configuration

app = Flask(__name__)

app.register_blueprint(client_configuration)


@app.route('/')
def hello_world():
	return 'Hello World!'


if __name__ == '__main__':
	port = JSONHandler.load("port", False, api_configuration_path)
	host = JSONHandler.load("host", False, api_configuration_path)
	app.run(port=port, host=host)
