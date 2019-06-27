curl -X PUT "localhost:9200/my_index" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_analyzer": {
          "tokenizer": "my_tokenizer",
	  "filter": [
	  	"lowercase"
	  ]
        }
      },
      "tokenizer": {
        "my_tokenizer": {
          "type": "ngram",
          "min_gram": 3,
          "max_gram": 3
        }
      }
    }
  },
  "mappings":{
       "properties":{
          "author": {
             "type":"text"
          },
	        "title": {
             "type":"text"
          },
          "chapter": {
             "type":"text"
          },
          "date": {
             "type":"date"
          },
          "location": {
             "type":"text"
          },
          "latin": {
             "type":"text"
          },
          "content": {
             "type":"text"
          },
          "comment": {
             "type":"text"
          },
          "material": {
             "type":"keyword"
          },
          "references": {
             "properties": {
              "edition": { "type": "text" },
              "translation":  { "type": "text" },
              "studies": {"type": "text"}
            }
          },
          "keys": {
             "type":"keyword"
          },
          "path": {
             "type":"text",
             "index": false
          }
      }
   }

}
'

