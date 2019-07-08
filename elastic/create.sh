curl -X DELETE "localhost:9200/my_index"
curl -X PUT "localhost:9200/my_index" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_analyzer": {
          "tokenizer": "standard",
      	  "filter": [
      	  	"lowercase"
      	  ]
        }
      },
      "tokenizer": {
        "my_tokenizer": {
          "type": "ngram",
          "min_gram": 2,
          "max_gram": 3
        }
      }
    }
  },
  "mappings":{
       "properties":{
          "author": {
             "type":"text",
             "analyzer": "my_analyzer"
          },
	        "title": {
             "type":"text",
             "analyzer": "my_analyzer"
          },
          "chapter": {
             "type":"text",
             "analyzer": "my_analyzer"
          },
          "date": {
             "type":"date"
          },
          "location": {
             "type":"text",
             "analyzer": "my_analyzer"
          },
          "latin": {
             "type":"text",
             "analyzer": "my_analyzer"
          },
          "content": {
             "type":"text",
             "analyzer": "my_analyzer"
          },
          "comment": {
             "type":"text",
             "analyzer": "my_analyzer"
          },
          "material": {
             "type":"keyword"
          },
          "references": {
             "properties": {
              "edition": { 
                  "type": "text",
                  "analyzer": "my_analyzer" 
              },
              "translation":  { 
                "type": "text",
                "analyzer": "my_analyzer"
              },
              "studies": {
                "type": "text",
                "analyzer": "my_analyzer"
              }
            }
          },
          "keys": {
             "type":"keyword"
          },
          "path": {
             "type":"text",
             "index": false
          },
          "added": {
             "type":"date"
          }
      }
   }

}
'

