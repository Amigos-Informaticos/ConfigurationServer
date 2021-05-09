import json

from flask import Blueprint, Response, request

from src.Configuration.JSONHandler import JSONHandler
from src.Configuration.Paths import data_dir_path

client_configuration = Blueprint("client_configuration", __name__)


@client_configuration.route("/<client>", methods=["POST"])
def save(client: str):
	payload = request.json
	status = 400
	if payload is not None:
		saved: bool = True
		for key in payload:
			if not JSONHandler.save(key, payload[key], data_dir_path + client + ".json"):
				saved = False
				break
		status = 201 if saved else 406
	return Response(status=status)


@client_configuration.route("/<client>", methods=["GET"])
def get_values(client: str):
	payload = request.json
	response = Response(status=404)
	if payload is not None:
		got: bool = True
		response_payload: dict = {}
		for key in payload:
			value = JSONHandler.load(key, True, data_dir_path + client + ".json")
			if value is not None:
				response_payload[key] = value
			else:
				got = False
				break
		if got:
			response = Response(
				json.dumps(response_payload),
				status=200,
				mimetype="application/json"
			)
		else:
			response = Response(status=404)
	return response


@client_configuration.route("/<client>/<resource>", methods=["GET"])
def get_value(client: str, resource):
	value = JSONHandler.load(resource, True, data_dir_path + client + ".json")
	response = Response(status=404)
	if value is not None:
		response = Response(
			json.dumps(value),
			status=200,
			mimetype="application/json"
		)
	return response


@client_configuration.route("/<client>/<resource>", methods=["DELETE"])
def delete_value(client: str, resource: str):
	if JSONHandler.delete(resource, data_dir_path + client + ".json"):
		response = Response(status=200)
	else:
		response = Response(status=404)
	return response
