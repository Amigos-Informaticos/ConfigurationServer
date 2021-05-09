from flask import Flask

from src.Configuration.JSONHandler import JSONHandler
from src.Configuration.Paths import api_configuration_path
from src.routes.ClientConfiguration import client_configuration

app = Flask(__name__)

app.register_blueprint(client_configuration)


@app.route('/')
def hello_world():
	return 'Hello World!'


def configure_app() -> tuple:
	returned_port = JSONHandler.load("port", False, api_configuration_path)
	returned_host = JSONHandler.load("host", False, api_configuration_path)
	return returned_port, returned_host


def run_app():
	port, host = configure_app()
	app.run(port=port, host=host)


if __name__ == '__main__':
	run_app()
