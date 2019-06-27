import os	
import hashlib

from elasticsearch import Elasticsearch

es = Elasticsearch()

def add_elastic(file_data):
	e1 = {
		"author": "Picasso",
	    "title": "Trojuholniky",
	    "chapter": "1",
	    "date": "2015-01-01",
	    "location": "France",
	    "latin": "Spiritus sanctis",
	    "content": "Prelozene vecicky",
	    "comment": "To znamena ze toto hento",
	    "material": "wall painting",
	    "references.edition": "Bib1",
	    "references.translation": "Bib2",
	    "references.studies": "Bib3",
	    "keys": ["patronage","fabricating"],
	    "path": "/static/photo.jpeg"
	}
	string_id = e1["title"]+e1["date"]+e1["content"]
	
	hash_id = hashlib.md5(string_id.encode('utf-8'))

	res = es.index(index='my_index',id=hash_id.hexdigest(),body=e1)
	if res == False:
		print("Add to index failed")


def delete_elastic(id):
	res=es.delete(index='my_index',id=id)
	if res['result'] != "deleted":
		print("Delete from index failed")

def get_elastic(id):
	results = es.get(index='my_index', id=id)
	print(results)
	return results


def search_elastic(query):
	# "query": {
	#     "multi_match" : {
	#       "query":    "Picasso",
	#       "fields": [ "author", "title", "chapter", "location", "latin", "content", "comment", "material", "references.*", "keys" ] 
	#     }
	#   },
	q = "o"

	query = {

		"query": { 
		    "bool": { 
				"should": [
					{ "match": { "author": q }}, 
					{ "match": { "title": q }},  
				],
				"filter": {
					"bool": {
					    "should": [
							{ "term": { "keys": "patronage" }},
							{ "term": { "keys": "d" }}
					    ]
					}
				}
		    }
		},	  
		  
		"highlight" : {
				"order" : "score",
		    "pre_tags" : ["<b>"],
		    "post_tags" : ["</b>"],
		    "fields" : {
		        "author" : {},
		        "title" : {},
		        "chapter" : {},
		        "location" : {},
		        "latin" : {},
		        "content" : {},
		        "comment" : {},
		        "material" : {},
		        "references.*" : {},
		        "keys" : {}
		    }
		}
	}

	results = es.search(index='my_index',body=query)
	print(results['hits']['hits'])
	return results['hits']['hits']

