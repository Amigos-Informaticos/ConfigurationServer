import json

from flask import Blueprint, Response, request

from src.Configuration.Connection import Connection

client_configuration = Blueprint("client_configuration", __name__)


@client_configuration.route("/<client>", methods=["GET"])
def get_client_document(client: str):
	response = Response(status=404)
	connection = Connection()
	document = connection.get_document_by_client(client)
	if document is not None:
		response = Response(
			json.dumps(document),
			status=200,
			mimetype="application/json"
		)
	return response


@client_configuration.route("/<client>", methods=["POST"])
def save(client: str):
	payload = request.json
	response = Response(status=404)
	if payload is not None:
		saved: bool = True
		connection = Connection()
		for key in payload:
			if not connection.save(client, key, payload[key]):
				saved = False
				break
		if saved:
			response = Response(
				json.dumps(connection.get_document_by_client(client)),
				status=201,
				mimetype="application/json"
			)
		else:
			response = Response(status=406)
	return response


@client_configuration.route("/<client>", methods=["PATCH"])
def get_values(client: str):
	payload = request.json
	response = Response(status=404)
	if payload is not None:
		got: bool = True
		response_payload: dict = {}
		connection = Connection()
		document = connection.get_document_by_client(client)
		if document is not None:
			for key in payload:
				if key in document:
					response_payload[key] = document[key]
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
	response = Response(status=404)
	value = Connection().get(client, resource, True)
	if value is not None:
		response = Response(
			json.dumps(value),
			status=200,
			mimetype="application/json"
		)
	return response


@client_configuration.route("/<client>/<resource>", methods=["DELETE"])
def delete_value(client: str, resource: str):
	if Connection().delete_resource_by_client(client, resource):
		response = Response(status=200)
	else:
		response = Response(status=404)
	return response


@client_configuration.route("/<client>", methods=["DELETE"])
def delete_client(client: str):
	connection = Connection()
	response = Response(status=404)
	if connection.delete_by_client(client):
		response = Response(status=200)
	return response
