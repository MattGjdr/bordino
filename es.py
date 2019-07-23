import os	
import hashlib
import elasticsearch
import datetime

from elasticsearch import Elasticsearch
from utils import convert_year

es = Elasticsearch()

"""
    Function add data to elasticsearch
"""
def add_elastic(file_data):
	
	print(file_data)

	string_id = file_data["title"]+file_data["date"]+file_data["content"]
	
	hash_id = hashlib.md5(string_id.encode('utf-8'))

	try:
		res = es.index(index='my_index',id=hash_id.hexdigest(),body=file_data)
	except elasticsearch.ElasticsearchException as es1:
		print('error add')

	if res == False:
		print("Add to index failed")

"""
    Function delete data from elasticsearch based on id
"""
def delete_elastic(id):
	try:
		res=es.delete(index='my_index',id=id)
	except elasticsearch.ElasticsearchException as es1:
		print('error delete')

	if res['result'] != "deleted":
		print("Delete from index failed")

"""
    Function get data from elasticsearch based on id
"""
def get_elastic(id):
	try:
		results = es.get(index='my_index', id=id)
	except elasticsearch.ElasticsearchException as es1:
		print('error get')

	print(results)
	return results

"""
    Function search data in elasticsearch based on given query
    Also other arguments are considered during creation of elastic body query
"""
def search_elastic(query,search_type,start,size):
	
	element_list = [ "author", "title", "chapter", "location", "latin", "content", "comment", "material","references.studies","references.edition","references.translation", "keys" ]
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

	#todo
	#DATE RANGE
	# print(query_list)
	# query_list.append({
	# 	"range" : {
 #            "date" : {
 #            	"format": "yyyy",					         
 #                "gte" : year_from,
 #                "lte" : year_to
 #            }
 #        }
	# })

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
					    "should": key_list
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
	print("===========query==========")
	print(query)
	print("========================")
	try:
		results = es.search(index='my_index',body=query)
	except:
		print('error searching')
		return []

	print(results)
	return results

"""
    Function add new data (args) to elasticsearch based on id
"""
def update_elastic(id, args):
	print(args)
	try:
		es.update(index='my_index',id=id, body={"doc": args})
	except:
		print('error updating')