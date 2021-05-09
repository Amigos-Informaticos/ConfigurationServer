import json
from os import path
from typing import Any

from src.Configuration.Paths import data_dir_path


class JSONHandler:
	@staticmethod
	def save(key: str, value: Any, file_path: str = data_dir_path) -> bool:
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
	def load(key: str, as_dict: bool = False, file_path: str = data_dir_path) -> Any:
		value: Any = None
		if path.exists(file_path):
			contents = json.load(open(file_path))
			if key in contents:
				value = contents[key]
				if as_dict:
					value = {key: value}
		return value

	@staticmethod
	def delete(key: str, file_path: str = data_dir_path) -> bool:
		deleted = False
		if path.exists(file_path):
			contents = json.load(open(file_path))
			if key in contents:
				contents.pop(key)
				with open(file_path, "w") as json_file:
					json.dump(contents, json_file, indent=2)
					deleted = True
		return deleted
