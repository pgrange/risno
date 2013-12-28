from pyes import *
conn = ES('127.0.0.1:9200') # Use HTTP

index = "immo2"
try:
  conn.indices.delete_index(index)
except:
  pass

conn.indices.create_index(index)

mapping = {
  'url': {'index': 'not_analyzed', 'type': 'string'},
  'img': {'index': 'not_analyzed', 'type': 'string'},
  'location': {'type': 'string'},
  'description': {'type': 'string'},
  'cities': {'type': 'string'},
  'price': {'type': 'integer'},
  'date': {'type': 'date'}}

conn.indices.put_mapping(index, {'properties':mapping}, ["immo"])
