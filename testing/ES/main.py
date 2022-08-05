import json

import requests

es_uri = 'http://192.168.31.188:9200'


def schema_mapper(es_uri, index_name, schema_name):
	available_schemas = ['object_db_schema', 'word_db_schema']
	success_status = "<Response [200]>"

	f = open('schema.json', 'r')
	mappings = json.load(f)

	try:
		specific_schema = mappings[schema_name]
	except KeyError:
		print(f"Schema not found from available schemas: {available_schemas}")
		return

	# print(json.dumps(specific_schema, indent=2))

	schema_uri = es_uri + "/" + index_name

	schema_stat = requests.put(schema_uri, json=specific_schema)

	schema_stat = json.dumps(str(schema_stat))

	print(schema_stat)

	check_stat = requests.get(schema_uri + "/_settings")
	check_stat = json.dumps(str(check_stat))
	print(check_stat)

	if "200" in str(schema_stat) and "200" in str(check_stat):
		print(f"Index {index_name} with {schema_name} schema successfully created and verified!")
	elif "200" in str(schema_stat) and "200" not in str(check_stat):
		print(f'Error creating index {index_name} with {schema_name} schema! Perhaps request was incorrectly formed or '
		      f'ElasticSearch Server is unreachable.')
	elif "200" not in str(schema_stat) and "200" in str(check_stat):
		print(f'Error creating index {index_name} with {schema_name} schema! The schema named {schema_name} likely '
		      f'already exists.')
	else:
		print(f'Error creating index {index_name} with {schema_name} schema! Perhaps request was incorrectly formed or '
		      f'ElasticSearch Server is unreachable.')


def add_doc(es_uri, index_name, data_type, data, update="add"):
	data_type_valid = ['object_db_schema', 'word_db_schema']
	if data_type not in data_type_valid:
		raise ValueError(f"Data type {data_type} not found in available data types: {data_type_valid}")

	update_valid = ["add", "concatenate", "overwrite", "blind"]
	if update not in update_valid:
		raise ValueError(f"Data type {data_type} not found in available data types: {update_valid}")

	success_status = "<Response [200]>"

	if data_type == 'object_db_schema':
		index_check = requests.get(es_uri + "/" + index_name)
		index_check = json.dumps(str(index_check))
		if "200" not in str(index_check):
			raise RuntimeError(f"Index {index_name} not found!")

		try:
			name = data['name']
			description = data['description']
			users = data['users']
			related_objects = data['related_objects']
			locations = data['locations']
		except KeyError:
			raise RuntimeError("Improperly formatted data. Data MUST be in the following format: {name: str, "
			                   "description: str, users: list, related_objects: list, locations: list}")

		queries_file = open('queries.json', 'r')
		queries = json.load(queries_file)

		queries["object_exists"]["query"]["query_string"]["query"] = name

		object_exists = requests.post(es_uri + "/" + index_name + "/_search", json=queries["object_exists"])
		object_exists_simple = json.dumps(str(object_exists))
		object_exists_full = json.loads(str(object_exists.text))

		print(object_exists_full["hits"]["total"]["value"])

		if "200" in object_exists_simple and object_exists_full["hits"]["total"]["value"] > 0 and update != "add":
			print(f"Object {name} already exists in index {index_name}!")
			if object_exists_full["hits"]["total"]["value"] > 1:
				raise RuntimeError("Search for existing objects failed and returned more than one result.")

			hit = object_exists_full["hits"]["hits"][0]
			hit_id = hit["_id"]
			hit_source = hit["_source"]

			print(type(hit_source["users"]))

			if update == "concatenate" or update == "blind":
				hit_source["name"] = name
				hit_source["description"] += description
				hit_source["users"] += users
				hit_source["related_objects"] += related_objects
				hit_source["locations"] += locations
			elif update == "overwrite":
				hit_source["name"] = name
				hit_source["description"] = description
				hit_source["users"] = users
				hit_source["related_objects"] = related_objects
				hit_source["locations"] = locations

			hit_source = json.dumps(hit_source)
			print(hit_source)
			hit_source = """{"doc":""" + hit_source + "}"
			print(hit_source)
			hit_source = json.loads(hit_source)
			print(hit_source)

			update_uri = es_uri + "/" + index_name + "/_update/" + hit_id
			update_stat = requests.post(update_uri, json=hit_source)
			print(update_stat.text)


		elif "200" in object_exists_simple and object_exists_full["hits"]["total"]["value"] == 0 and update == "add":
			print(f"Object {name} does not exist in index {index_name}! Proceeding to add object...")

			data_uri = es_uri + "/" + index_name + "/_doc"
			data_stat = requests.post(data_uri, json=data)
			data_stat = json.dumps(str(data_stat))

			print(data_stat)

			if "201" in str(data_stat):
				print(f"Object {name} successfully added to index {index_name}!")
			else:
				print(f"Error adding object {name} to index {index_name}!")
		else:
			print(f"Error checking if object {name} exists in index {index_name}!")

	elif data_type == 'word_db_schema':
		index_check = requests.get(es_uri + "/" + index_name)
		index_check = json.dumps(str(index_check))
		if "200" not in str(index_check):
			raise RuntimeError(f"Index {index_name} not found!")

		try:
			word = data['word']
			definition = data['definition']
			users = data['users']
			related_words = data['related_words']
			related_objects = data['related_objects']
			locations = data['locations']
		except KeyError:
			raise RuntimeError("Improperly formatted data. Data MUST be in the following format: {name: str, "
			                   "description: str, users: list, related_objects: list, locations: list}")

		queries_file = open('queries.json', 'r')
		queries = json.load(queries_file)

		queries["word_exists"]["query"]["query_string"]["query"] = word

		word_exists = requests.post(es_uri + "/" + index_name + "/_search", json=queries["word_exists"])
		word_exists_simple = json.dumps(str(word_exists))
		word_exists_full = json.loads(str(word_exists.text))

		print(word_exists_full["hits"]["total"]["value"])

		if "200" in word_exists_simple and word_exists_full["hits"]["total"]["value"] > 0 and update != "add":
			print(f"Object {word} already exists in index {index_name}!")
			if word_exists_full["hits"]["total"]["value"] > 1:
				raise RuntimeError("Search for existing objects failed and returned more than one result.")

			hit = word_exists_full["hits"]["hits"][0]
			hit_id = hit["_id"]
			hit_source = hit["_source"]

			print(type(hit_source["users"]))

			if update == "concatenate" or update == "blind":
				hit_source["word"] += word
				hit_source["description"] += definition
				hit_source["users"] += users
				hit_source["related_objects"] += related_objects
				hit_source["related_words"] += related_words
				hit_source["locations"] += locations
			elif update == "overwrite":
				hit_source["word"] = word
				hit_source["description"] = definition
				hit_source["users"] = users
				hit_source["related_objects"] = related_objects
				hit_source["related_words"] = related_words
				hit_source["locations"] = locations

			hit_source = json.dumps(hit_source)
			print(hit_source)
			hit_source = """{"doc":""" + hit_source + "}"
			print(hit_source)
			hit_source = json.loads(hit_source)
			print(hit_source)

			update_uri = es_uri + "/" + index_name + "/_update/" + hit_id
			update_stat = requests.post(update_uri, json=hit_source)
			print(update_stat.text)


		elif "200" in word_exists_simple and word_exists_full["hits"]["total"]["value"] == 0 and update == "add":
			print(f"Object {word} does not exist in index {index_name}! Proceeding to add object...")

			data_uri = es_uri + "/" + index_name + "/_doc"
			data_stat = requests.post(data_uri, json=data)
			data_stat = json.dumps(str(data_stat))

			print(data_stat)

			if "201" in str(data_stat):
				print(f"Object {word} successfully added to index {index_name}!")
			else:
				print(f"Error adding object {word} to index {index_name}!")
		else:
			print(f"Error checking if object {word} exists in index {index_name}!")


# schema_mapper(es_uri, "testdb1", "object_db_schema")
# f = open('queries.json', 'r')
# queries = json.load(f)
#
# print(json.dumps(queries["object_exists"], indent=2))

add_doc(es_uri, "testdb1", "object_db_schema",
        {"name": "bananabanana", "description": "l", "users": ["l"],
         "related_objects": ["l"], "locations": ["l"]}, update="overwrite")

