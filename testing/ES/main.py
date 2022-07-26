import json

import requests

es_uri = 'http://192.168.31.188:9200'

stat = requests.get(es_uri + "/_all")
#
print(stat.json())


def schema_mapper(es_uri, index_name, schema_name):
	available_schemas = ['object_db_schema', 'word_db_schema']
	success_status = "<Response [200]>"

	f = open('schema_nested.json', 'r')
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

	if schema_stat == success_status:
		print(f"Index {index_name} with {schema_name} schema successfully created!")
	else:
		print(f"Error creating index {index_name} with {schema_name} schema! Perhaps request was incorrectly formed or "
		      f"ElasticSearch Server is unreachable.")


schema_mapper(es_uri, "c", "object_db_schema")
