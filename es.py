import os	
import hashlib
import elasticsearch
import datetime

from elasticsearch import Elasticsearch
from utils import convert_year

es = Elasticsearch()

def add_elastic(file_data):
	now = datetime.datetime.now()

	e1 = {
		"author": "Textovty monet",
	    "title": "Kruhyyyy textu",
	    "chapter": "1",
	    "date": "2015-01-01",
	    "location": "France",
	    "latin": "Spiritus sanctis",
	    "content": "Ine vecicky",
	    "comment": "To znamena ze toto hento",
	    "material": "wall painting",
	    "references.edition": "Bib1",
	    "references.translation": "Bib2",
	    "references.studies": "Bib3",
	    "keys": ["patronage","kissing"],
	    "path": "",
	    "added": now.strftime("%Y-%m-%d")
	}

	string_id = e1["title"]+e1["date"]+e1["content"]
	
	hash_id = hashlib.md5(string_id.encode('utf-8'))

	try:
		res = es.index(index='my_index',id=hash_id.hexdigest(),body=e1)
	except elasticsearch.ElasticsearchException as es1:
		print('error add')

	if res == False:
		print("Add to index failed")


def delete_elastic(id):
	try:
		res=es.delete(index='my_index',id=id)
	except elasticsearch.ElasticsearchException as es1:
		print('error delete')

	if res['result'] != "deleted":
		print("Delete from index failed")

def get_elastic(id):
	try:
		results = es.get(index='my_index', id=id)
	except elasticsearch.ElasticsearchException as es1:
		print('error get')

	print(results)
	return results


def search_elastic(query,search_type,start,size):
	# "query": {
	#     "multi_match" : {
	#       "query":    "Picasso",
	#       "fields": [ "author", "title", "chapter", "location", "latin", "content", "comment", "material", "references.*", "keys" ] 
	#     }
	#   },
	element_list = [ "author", "title", "chapter", "location", "latin", "content", "comment", "material", "references.*" ]
	#keys different parsing
	query_list = []
	key_list = []

	#@TODO DATE FORMAT

	date_range = query.get("date","1-now")
	date_range = "".join(date_range.split())
	if '-' in date_range:
		year_from = convert_year(date_range.split("-")[0])
		year_to = convert_year(date_range.split("-")[1])
	else:
		year_from = date_range
		year_to = date_range

	if search_type == "all":
		print("Error type not specified")
		query = {
			"from": start, "size": size,
			"sort": [
				{ "added" : {"order" : "desc"}},
        		"_score"
			],
		    "query": {
		        "match_all": {}
		    }
		}
		try:
			results = es.search(index='my_index',body=query)
		except:
			print('error searching')
		return results

	else:
		if search_type == "basic":
			for e in element_list:
				query_list.append({ "fuzzy": { e: query.get("q","") }})
		else:
			for e in element_list:
				if query.get(e):
					query_list.append({ "fuzzy": { e: query.get(e,"") }})


	# query_list.append({
	# 	"aggs": {
	#         "range": {
	#             "date_range": {
	#                 "field": "date",
	#                 "format": "yyyy",
	#                 "ranges": [
	#                     { "to": "2000" }, 
	#                     { "from": "1900" } 
	#                 ]
	#             }
	#         }
	#     }
	# })

	print(query_list)

	if query.get("keys"):
		keys = query.get("keys","").split(",")
		for k in keys:
			key_list.append({ "term": { "keys": k }})

	print(key_list)

	filter_field = "random_field_value"
	must_field = "must_not"
	if search_type == "text":
		must_field = "must_not"
		filter_field = "path"

	if search_type == "image":
		must_field = "must"
		filter_field = "path"



	query = {
		"from": start, "size": size,
		"query": { 
		    "bool": { 
				"should": query_list,
				must_field: {
	                "exists": {
	                    "field": filter_field
	                }
	            },
				"filter": {
					"bool": {
					    "should": key_list,
					    "must": {
							"range" : {
					            "date" : {
					            	"format": "yyyy",					         
					                "gte" : year_from,
					                "lte" : year_to
					            }
					        }
					    }
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

	print(query)
	#todo problem s highglight ak je ngram
	try:
		results = es.search(index='my_index',body=query)
	except:
		print('error searching')
		return []

	print(results)
	return results

def update_elastic(id, args):
	print(args)
	try:
		es.update(index='my_index',id=id, body={"doc": args})
	except:
		print('error updating')