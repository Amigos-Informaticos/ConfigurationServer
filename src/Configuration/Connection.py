from typing import Any, Optional

from pymongo import MongoClient
from pymongo.collection import Collection

from src.Configuration.JSONHandler import JSONHandler
from src.Configuration.Paths import api_configuration_path


class Connection:
	def __init__(self, connection: str = "connection_string", path: str = api_configuration_path):
		connection_string = JSONHandler.load(connection, False, path)
		self.connection = MongoClient(connection_string)
		self.database_name = "configuration_server"
		self.collection_name = "configuration"
		self.collection = self.connection[self.database_name][self.collection_name]

	def save(self, client: str, key: str, value: Any) -> bool:
		saved: bool = False
		if Connection.document_exists(self.collection, {"client": client}):
			self.collection.update_one(
				{"client": client},
				{"$set": {key: value}}
			)
			saved = True
		else:
			self.collection.insert_one({
				"client": client,
				key: value
			})
			saved = True
		return saved

	def get(self, client: str, key: str, as_dict: bool = False) -> Any:
		value: Any = None
		if Connection.document_exists(self.collection, {"client": client}):
			contents = self.collection.find_one({"client": client})
			if key in contents:
				value = contents[key]
				if as_dict:
					value = {key: value}
		return value

	def get_document_by_client(self, client: str) -> Optional[dict]:
		document: Optional[dict] = None
		if Connection.document_exists(self.collection, {"client": client}):
			document = self.collection.find_one({"client": client})
		return document

	def delete_resource_by_client(self, client: str, resource: str) -> bool:
		deleted: bool = False
		document = self.get_document_by_client(client)
		if document is not None:
			document.pop(resource)
			self.collection.update_one(
				{"client": client},
				{"$set": document}
			)
			deleted = True
		return deleted

	def delete_by_client(self, client: str) -> bool:
		deleted: bool = False
		if Connection.document_exists(self.collection, {"client": client}):
			self.collection.remove({"client": client})
			deleted = True
		return deleted

	@staticmethod
	def document_exists(collection: Collection, criteria: dict) -> bool:
		return collection.count_documents(criteria)

	@staticmethod
	def get_connection(value: str = "connection_string", path: str = api_configuration_path):
		return MongoClient(JSONHandler.load(value, False, path))
