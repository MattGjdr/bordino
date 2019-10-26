curl -X DELETE "localhost:9200/my_index"
curl -X PUT "localhost:9200/my_index" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "analysis": {
      "filter": {
        "my_stop": {
            "type": "stop",
            "stopwords":  "_english_"
        }
      },
      "analyzer": {
        "my_analyzer": {
          "tokenizer": "standard",
      	  "filter": [
      	  	"lowercase",
            "my_stop"
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
             "type":"integer_range"
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
          "type": {
             "type":"text",
             "analyzer": "my_analyzer"
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
              },             
              "photo": {
                "type": "text",
                "analyzer": "my_analyzer"
              }
            }
          },
          "keys": {
             "type":"keyword"
          },
          "path": {
             "type":"text" 
          },
          "added": {
             "type":"date"
          }
      }
   }

}
'

