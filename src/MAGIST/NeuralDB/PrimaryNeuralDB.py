import time

from ..Utils.LogMaster.log_init import MainLogger

class NeuralDB():
	def __init__(self, config, db_client):
		root_log = MainLogger(config)
		self.log = root_log.StandardLogger("NeuralDB")  # Create a script specific logging instance
		self.client = db_client

	def recreate_db(self):
		self.log.warning("NeuralDB is about to reset and recreate all Databases and tables. Proceeding in 5 seconds...")
		# 5 second countdown
		for i in range(5):
			self.log.warning("{}...".format(5 - i))
			time.sleep(1)
		self.log.warning("Resetting and recreating all databases and tables...")

		self.vision = self.client["VisionDB"]
		self.nlp = self.client["NLP"]
		self.common = self.client["Common"]

		self.dbs = [self.vision, self.nlp, self.common]

		self.obj_desc = self.vision["ObjectDesc"]
		self.obj_location = self.vision["ObjectLocation"]
		self.obj_obj_relation = self.vision["ObjectObjectRelation"]
		self.obj_users = self.vision["ObjectUsers"]

		self.word_desc = self.nlp["WordDesc"]
		self.word_location = self.nlp["WordLocation"]

		self.word_obj_relation = self.common["WordObjectRelation"]

	def insert_obj_desc(self, obj_name, obj_desc):
		self.log.info(f"Inserting object description: {obj_name} - {obj_desc}")
		self.obj_desc.insert_one({"obj_name": obj_name, "obj_desc": obj_desc})
	def insert_obj_location(self, obj_name, obj_location):
		self.log.info(f"Inserting object location: {obj_name} - {obj_location}")
		self.obj_location.insert_one({"obj_name": obj_name, "obj_location": obj_location})
	def insert_obj_obj_relation(self, obj_name, second_obj_name):
		self.log.info(f"Inserting object object relation: {obj_name} - {second_obj_name}")
		self.obj_obj_relation.insert_one({"obj_name": obj_name, "second_obj_name": second_obj_name})
	def insert_obj_users(self, obj_name, user_name):
		self.log.info(f"Inserting object users: {obj_name} - {user_name}")
		self.obj_users.insert_one({"obj_name": obj_name, "user_name": user_name})

	def insert_word_desc(self, word_name, word_desc):
		self.log.info(f"Inserting word description: {word_name} - {word_desc}")
		self.word_desc.insert_one({"word_name": word_name, "word_desc": word_desc})
	def insert_word_location(self, word_name, word_location):
		self.log.info(f"Inserting word location: {word_name} - {word_location}")
		self.word_location.insert_one({"word_name": word_name, "word_location": word_location})
	def insert_word_obj_relation(self, word_name, obj_name):
		self.log.info(f"Inserting word object relation: {word_name} - {obj_name}")
		self.word_obj_relation.insert_one({"word_name": word_name, "word_relation": obj_name})

	def search_obj_details(self, obj_name):
		data = []
		self.log.info(f"Searching object details: {obj_name}")

		for d in self.dbs:
			self.log.info(f"===> Database: {d.name}")

			for i in d.list_collection_names():
				self.log.info(f"    ===> Collection: {i}")
				for j in self.vision[i].find({"obj_name": {"$regex": obj_name}}):
					self.log.info(f"        ===> {j}")
					data.append(j)
		return data

	def search_obj_desc(self, keyword):
		data = []
		self.log.info(f"Searching object details by keyword: {keyword}")

		for d in self.dbs:
			self.log.info(f"===> Database: {d.name}")

			for i in d.list_collection_names():
				self.log.info(f"    ===> Collection: {i}")
				for j in self.vision[i].find({"obj_desc" : {"$regex" : keyword}}):
					self.log.info(f"        ===> {j}")
					data.append(j)
		return data

	def search_obj_location(self, location):
		data = []
		self.log.info(f"Searching object details by location: {location}")

		for d in self.dbs:
			self.log.info(f"===> Database: {d.name}")

			for i in d.list_collection_names():
				self.log.info(f"    ===> Collection: {i}")
				for j in self.vision[i].find({"obj_location" : {"$regex" : location}}):
					self.log.info(f"        ===> {j}")
					data.append(j)
		return data

	def search_obj_user(self, user):
		data = []
		self.log.info(f"Searching object details by user: {user}")

		for d in self.dbs:
			self.log.info(f"===> Database: {d.name}")

			for i in d.list_collection_names():
				self.log.info(f"    ===> Collection: {i}")
				for j in self.vision[i].find({"user_name" : {"$regex" : user}}):
					self.log.info(f"        ===> {j}")
					data.append(j)
		return data





	def search_word_details(self, word):
		data = []
		self.log.info(f"Searching word details: {word}")

		for d in self.dbs:
			self.log.info(f"===> Database: {d.name}")

			for i in d.list_collection_names():
				self.log.info(f"    ===> Collection: {i}")
				for j in self.vision[i].find({"word_name" : {"$regex" : word}}):
					self.log.info(f"        ===> {j}")
					data.append(j)
		return data

	def search_word_desc(self, keyword):
		data = []
		self.log.info(f"Searching word details by keyword: {keyword}")

		for d in self.dbs:
			self.log.info(f"===> Database: {d.name}")

			for i in d.list_collection_names():
				self.log.info(f"    ===> Collection: {i}")
				for j in self.vision[i].find({"word_desc" : {"$regex" : keyword}}):
					self.log.info(f"        ===> {j}")
					data.append(j)
		return data

	def search_word_location(self, location):
		data = []
		self.log.info(f"Searching word details by location: {location}")

		for d in self.dbs:
			self.log.info(f"===> Database: {d.name}")

			for i in d.list_collection_names():
				self.log.info(f"    ===> Collection: {i}")
				for j in self.vision[i].find({"word_location" : {"$regex" : location}}):
					self.log.info(f"        ===> {j}")
					data.append(j)
		return data

	def search_word_relation(self, relation):
		data = []
		self.log.info(f"Searching word details by relation: {relation}")

		for d in self.dbs:
			self.log.info(f"===> Database: {d.name}")

			for i in d.list_collection_names():
				self.log.info(f"    ===> Collection: {i}")
				for j in self.vision[i].find({"word_relation" : {"$regex" : relation}}):
					self.log.info(f"        ===> {j}")
					data.append(j)
		return data

