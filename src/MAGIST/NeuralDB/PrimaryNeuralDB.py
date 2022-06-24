"""Main NeuralDB updating and querying class

This class contains functions necessary to add information to the NeuralDB as well as query it for information upon
request. This requires the instantiated client from MongoUtils.
"""

import json
import pathlib
import time
import re

from ..Utils.LogMaster.log_init import MainLogger


class NeuralDB():
	"""Main NeuralDB class"""
	def __init__(self, config, db_client):
		"""Initialize NeuralDB class, parse config.json, and receive MongoDB client

		:param config: The config(config.json) file as a string.
		:param db_client: The MongoDB client from MongoUtils.
		"""

		root_log = MainLogger(config)
		self.log = root_log.StandardLogger("NeuralDB")  # Create a script specific logging instance
		self.client = db_client

		config = pathlib.Path(config)
		config = config.resolve()  # Find absolute path from a relative one.
		f = open(config)
		config = json.load(f)

		for i in config['neural_db']:
			try:
				self.db_string = i["db_search_zone"]
			except KeyError:
				pass

	def recreate_db(self):
		"""Recreate the databases and collections
		"""

		self.log.warning("NeuralDB is about to reset and recreate all Databases and tables. Proceeding in 5 seconds...")

		for i in range(5):
			self.log.warning("{}...".format(5 - i))
			time.sleep(1)
		self.log.warning("Resetting and recreating all databases and tables...")

		self.dbs = []
		self.collections = []

		for d in self.db_string:
			if d == "vision":
				self.vision = self.client['VisionDB']

				self.obj_desc = self.vision["ObjectDesc"]
				self.obj_location = self.vision["ObjectLocation"]
				self.obj_obj_relation = self.vision["ObjectObjectRelation"]
				self.obj_users = self.vision["ObjectUsers"]

				self.log.info("Vision database is included in NeuralDB search.")

				self.dbs.append(self.vision)

				self.collections.append(self.obj_desc)
				self.collections.append(self.obj_location)
				self.collections.append(self.obj_obj_relation)
				self.collections.append(self.obj_users)
			if d == "nlp":
				self.nlp = self.client["NLP"]

				self.word_desc = self.nlp["WordDesc"]
				self.word_location = self.nlp["WordLocation"]

				self.log.info("NLP database is included in NeuralDB search.")

				self.dbs.append(self.nlp)

				self.collections.append(self.word_desc)
				self.collections.append(self.word_location)
			if d == "common":
				self.common = self.client["Common"]

				self.word_obj_relation = self.common["WordObjectRelation"]

				self.log.info("Common database is included in NeuralDB search.")

				self.dbs.append(self.common)

				self.collections.append(self.word_obj_relation)

		try:
			if self.vision is None:
				self.log.warning("Vision database was not included from NeuralDB search.")
		except AttributeError:
			self.log.warning("Vision database was not included from NeuralDB search.")

		try:
			if self.nlp is None:
				self.log.warning("NLP database was not included from NeuralDB search.")
		except AttributeError:
			self.log.warning("NLP database was not included from NeuralDB search.")

		try:
			if self.common is None:
				self.log.warning("Common database was not included from NeuralDB search.")
		except AttributeError:
			self.log.warning("Common database was not included from NeuralDB search.")

	def insert_obj_desc(self, obj_name, obj_desc):
		"""Insert object and its description into the Vision database.

		:param obj_name: The name of the object(string).
		:param obj_desc: The description of the object(string).
		"""

		self.log.info(f"Inserting object description: {obj_name} - {obj_desc}")
		self.obj_desc.insert_one({"obj_name": obj_name, "obj_desc": obj_desc})
	def insert_obj_location(self, obj_name, obj_location):
		"""Insert object and its location into the Vision database.

		:param obj_name: The name of the object(string).
		:param obj_location: The location of the object(string).
		"""
		self.log.info(f"Inserting object location: {obj_name} - {obj_location}")
		self.obj_location.insert_one({"obj_name": obj_name, "obj_location": obj_location})
	def insert_obj_obj_relation(self, obj_name, second_obj_name):
		"""Insert object and its relation to another object into the Vision database.

		:param obj_name: The name of the object(string).
		:param second_obj_name: The name of the second object(string).
		"""

		self.log.info(f"Inserting object object relation: {obj_name} - {second_obj_name}")
		self.obj_obj_relation.insert_one({"obj_name": obj_name, "second_obj_name": second_obj_name})
	def insert_obj_users(self, obj_name, user_name):
		"""Insert object and its users into the Vision database.

		:param obj_name: The name of the object(string).
		:param user_name: The name of the user(string).
		"""

		self.log.info(f"Inserting object users: {obj_name} - {user_name}")
		self.obj_users.insert_one({"obj_name": obj_name, "user_name": user_name})

	def insert_word_desc(self, word_name, word_desc):
		"""Insert word and its description into the NLP database.

		:param word_name: The name of the word(string).
		:param word_desc: The description of the word(string).
		"""

		self.log.info(f"Inserting word description: {word_name} - {word_desc}")
		self.word_desc.insert_one({"word_name": word_name, "word_desc": word_desc})
	def insert_word_location(self, word_name, word_location):
		"""Insert word and its location into the NLP database.

		:param word_name: The name of the word(string).
		:param word_location: The location of the word(string).
		"""

		self.log.info(f"Inserting word location: {word_name} - {word_location}")
		self.word_location.insert_one({"word_name": word_name, "word_location": word_location})
	def insert_word_obj_relation(self, word_name, obj_name):
		"""Insert word and its relation to an object into the NLP database.

		:param word_name: The name of the word(string).
		:param obj_name: The name of the object(string).
		"""

		self.log.info(f"Inserting word object relation: {word_name} - {obj_name}")
		self.word_obj_relation.insert_one({"word_name": word_name, "word_relation": obj_name})

	def search_obj_details(self, obj_name):
		"""Search for object all details in the Vision database.

		:param obj_name: The name of the object(string).

		:return: A dictionary containing the object details.
		"""

		data = []
		self.log.info(f"Searching object details: {obj_name}")

		for d in self.dbs:
			self.log.info(f"===> Database: {d.name}")

			for i in d.list_collection_names():
				self.log.info(f"    ===> Collection: {i}")
				for j in self.vision[i].find({"obj_name": re.compile(rf"\b{obj_name}\b", re.IGNORECASE)}):
					self.log.info(f"        ===> {j}")
					data.append(j)
		return data

	def search_obj_desc(self, keyword):
		"""Search for object descriptions by keyword in the Vision database.

		:param keyword: The keyword to search for(string).

		:return: A dictionary containing the object descriptions.
		"""

		data = []
		self.log.info(f"Searching object details by keyword: {keyword}")

		for d in self.dbs:
			self.log.info(f"===> Database: {d.name}")

			for i in d.list_collection_names():
				self.log.info(f"    ===> Collection: {i}")
				for j in self.vision[i].find({"obj_desc" : re.compile(rf"\b{keyword}\b", re.IGNORECASE)}):
					self.log.info(f"        ===> {j}")
					data.append(j)
		return data

	def search_obj_location(self, location):
		"""Search for object locations by location in the Vision database.

		:param location: The location to search for(string).

		:return: A dictionary containing the object locations.
		"""

		data = []
		self.log.info(f"Searching object details by location: {location}")

		for d in self.dbs:
			self.log.info(f"===> Database: {d.name}")

			for i in d.list_collection_names():
				self.log.info(f"    ===> Collection: {i}")
				for j in self.vision[i].find({"obj_location" : re.compile(rf"\b{location}\b", re.IGNORECASE)}):
					self.log.info(f"        ===> {j}")
					data.append(j)
		return data

	def search_obj_user(self, user):
		"""Search for object users by user in the Vision database.

		:param user: The user to search for(string).

		:return: A dictionary containing the object users.
		"""

		data = []
		self.log.info(f"Searching object details by user: {user}")

		for d in self.dbs:
			self.log.info(f"===> Database: {d.name}")

			for i in d.list_collection_names():
				self.log.info(f"    ===> Collection: {i}")
				for j in self.vision[i].find({"user_name" : re.compile(rf"\b{user}\b", re.IGNORECASE)}):
					self.log.info(f"        ===> {j}")
					data.append(j)
		return data





	def search_word_details(self, word):
		"""Search for word details in the NLP database.

		:param word: The word to search for(string).

		:return: A dictionary containing the word details.
		"""

		data = []
		self.log.info(f"Searching word details: {word}")

		for d in self.dbs:
			self.log.info(f"===> Database: {d.name}")

			for i in d.list_collection_names():
				self.log.info(f"    ===> Collection: {i}")
				for j in self.vision[i].find({"word_name" : re.compile(rf"\b{word}\b", re.IGNORECASE)}):
					self.log.info(f"        ===> {j}")
					data.append(j)
		return data

	def search_word_desc(self, keyword):
		"""Search for word descriptions by keyword in the NLP database.

		:param keyword: The keyword to search for(string).

		:return: A dictionary containing the word descriptions.
		"""

		data = []
		self.log.info(f"Searching word details by keyword: {keyword}")

		for d in self.dbs:
			self.log.info(f"===> Database: {d.name}")

			for i in d.list_collection_names():
				self.log.info(f"    ===> Collection: {i}")
				for j in self.vision[i].find({"word_desc" : re.compile(rf"\b{keyword}\b", re.IGNORECASE)}):
					self.log.info(f"        ===> {j}")
					data.append(j)
		return data

	def search_word_location(self, location):
		"""Search for word locations by location in the NLP database.

		:param location: The location to search for(string).

		:return: A dictionary containing the word locations.
		"""

		data = []
		self.log.info(f"Searching word details by location: {location}")

		for d in self.dbs:
			self.log.info(f"===> Database: {d.name}")

			for i in d.list_collection_names():
				self.log.info(f"    ===> Collection: {i}")
				for j in self.vision[i].find({"word_location" : re.compile(rf"\b{location}\b", re.IGNORECASE)}):
					self.log.info(f"        ===> {j}")
					data.append(j)
		return data

	def search_word_relation(self, relation):
		"""Search for word relations by relation in the NLP database.

		:param relation: The relation to search for(string).

		:return: A dictionary containing the word relations.
		"""

		data = []
		self.log.info(f"Searching word details by relation: {relation}")

		for d in self.dbs:
			self.log.info(f"===> Database: {d.name}")

			for i in d.list_collection_names():
				self.log.info(f"    ===> Collection: {i}")
				for j in self.vision[i].find({"word_relation" : re.compile(rf"\b{relation}\b", re.IGNORECASE)}):
					self.log.info(f"        ===> {j}")
					data.append(j)
		return data

	def remove_duplicates(self):
		_locals = locals()
		print(self.vision.ObjectDesc)
		for d in self.dbs:
			for i in d.list_collection_names():
				exec(f"db_col = self.client.{d.name}.{i}", _locals)
				db_col = _locals['db_col']

				repeated_val = ""

				if "vision" in d.name.lower():
					repeated_val = "obj_name"
					print("vision")
				if "nlp" in d.name.lower():
					repeated_val = "word_name"
					print("nlp")

				replic = db_col.aggregate([  # Cursor with all duplicated documents
					{'$group': {
						'_id': {repeated_val: f'${repeated_val}'},  # Duplicated field
						'uniqueIDs': {'$addToSet': '$_id'},
						'total': {'$sum': 1}
					}
					},
					{'$match': {
						'total': {'$gt': 1}  # Holds how many duplicates for each group, if you need it.
					}
					}
				])
				# Result is a list of lists of ObjectsIds
				for i in replic:
					print(i)
					for idx, j in enumerate(i['uniqueIDs']):  # It holds the ids of all duplicates
						if idx != 0:  # Jump over first element to keep it
							db_col.delete_one({'_id': j})

