from datetime import datetime
import elasticsearch_dsl as esdsl

client = esdsl.connections.connections.create_connection(hosts=['192.168.31.188'])

print(client.info())