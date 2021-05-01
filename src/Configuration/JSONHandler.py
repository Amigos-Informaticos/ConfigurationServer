import json
from os import path
from typing import Any


class JSONHandler:
	@staticmethod
	def save(file_path: str, key: str, value: Any) -> bool:
		saved: bool = False
		if path.exists(file_path):
			contents = json.load(open(file_path))
		else:
			contents: dict = {}
		contents[key] = value
		with open(file_path, "w") as json_file:
			json.dump(contents, json_file, indent=2)
			saved = True
		return saved

	@staticmethod
	def load(file_path: str, key: str) -> Any:
		value: Any = None
		if path.exists(file_path):
			contents = json.load(open(file_path))
			if key in contents:
				value = contents[key]
		return value
