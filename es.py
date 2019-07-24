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
		print(es1)

	if res == False:
		print("Add to index failed")

"""
    Function delete data from elasticsearch based on id
"""
def delete_elastic(id):
	try:
		res=es.delete(index='my_index',id=id)
	except elasticsearch.ElasticsearchException as es1:
		print(es1)

	if res['result'] != "deleted":
		print("Delete from index failed")

"""
    Function get data from elasticsearch based on id
"""
def get_elastic(id):
	try:
		results = es.get(index='my_index', id=id)
	except elasticsearch.ElasticsearchException as es1:
		print(es1)

	print(results)
	return results

def search_all(start, size, check_date):
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
	except elasticsearch.ElasticsearchException as es1:
		print(es1)
	return results, check_date

"""
    Function search data in elasticsearch based on given query
    Also other arguments are considered during creation of elastic body query
"""
def search_elastic(query,search_type,start,size):
	
	element_list = [ "date", "author", "title", "chapter", "location", "latin", "content", "comment", "material","references.studies","references.edition","references.translation" ]
	#keys different parsing
	query_list = []
	key_list = []

	query_bool = "should"
	#DATE check
	check_date = False

	date_range = query.get("date","1-now")
	date_range = "".join(date_range.split())
	if '-' in date_range:
		year_from = convert_year(date_range.split("-")[0])
		year_to = convert_year(date_range.split("-")[1])
	else:
		year_from = date_range
		year_to = date_range

	if search_type == "all":
		return search_all(start, size, check_date);

	else:
		if search_type == "basic":
			element_list.pop(0)
			for e in element_list:
				query_list.append({ "fuzzy": { e: query.get("q","") }})
		else:
			#if specific search then even REASEARCH KEYS are used as AND not as OR
			query_bool = "must"
			for e in element_list:
				if query.get(e):
					#IMPORTANT "date" should be first in element_list
					if (e == "date"):
						check_date = True
						query_list.append({
							"range" : {
						        "date" : {
						        	"format": "yyyy",					         
						            "gte" : year_from,
						            "lte" : year_to
						        }
						    }
						})
					#string/text type
					else:
						query_list.append({ "fuzzy": { e: query.get(e,"") }})


	#image / text filter, which should be searched, whether one or other or both
	exist_query = False

	if search_type == "text":
		exist_query = {
			"bool": {
				"must_not": [{
					"exists": {
						"field" : "path"
					}
				}]
			}
		}
	if search_type == "image":
		exist_query = {
			"exists": {
				"field" : "path"
			}
		}

	if query.get("keys"):
		keys = query.get("keys","").split(",")
		for k in keys:
			key_list.append({ "term": { "keys": k }})

	print(key_list)

	if exist_query:
		bool_query = {
			query_bool: [query_list, key_list],
			"filter": {
				"bool": {
				    "should": [exist_query]
				}
			}
		}
	else:
		bool_query = {
			query_bool: [query_list, key_list]
		}


	query = {
		"from": start, "size": size,
		"query": { 
		    "bool": bool_query
		},	  
		  
		"highlight" : {
			"order" : "score",
		    "pre_tags" : ["<b>"],
		    "post_tags" : ["</b>"],
		    "fields" : {
		        "*" : {}
		    }
		}
	}
	print("===========query==========")
	print(query)
	print("========================")
	try:
		results = es.search(index='my_index',body=query)
	except elasticsearch.ElasticsearchException as es1:
		print(es1)
		return [], check_date

	print(results)
	return results, check_date

"""
    Function add new data (args) to elasticsearch based on id
"""
def update_elastic(id, args):
	print(args)
	try:
		es.update(index='my_index',id=id, body={"doc": args})
	except elasticsearch.ElasticsearchException as es1:
		print(es1)