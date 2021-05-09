from flask import Flask

from src.routes.ClientConfiguration import client_configuration

app = Flask(__name__)

app.register_blueprint(client_configuration)


@app.route('/')
def hello_world():
	return 'Hello World!'


if __name__ == '__main__':
	app.run()
