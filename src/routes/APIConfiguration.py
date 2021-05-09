import json

from flask import Blueprint, Response, request

from src.Configuration.JSONHandler import JSONHandler
from src.Configuration.Paths import api_configuration_path

api_configuration = Blueprint("api_configuration", __name__)


@api_configuration.route("/grapi/save", methods=["POST"])
def savea():
	payload = request.json
	status = 400
	if payload is not None:
		saved: bool = True
		for key in payload:
			if not JSONHandler.save(api_configuration_path, key, payload[key]):
				saved = False
				break
		status = 201 if saved else 406
	return Response(status=status)


@api_configuration.route("/grapi/<key>", methods=["GET"])
def get_grapi_value(key: str):
	value = JSONHandler.load(key, True)
	status = 200 if value is not None else 404
	return Response(
		json.dumps(value),
		status=status,
		mimetype="application/json"
	)
