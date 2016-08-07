# Testing task
Please see [test_task_backend_dev.pdf (rus)](https://github.com/mario1ua/11.skein/blob/master/test_task_backend_dev.pdf) for task description

## Running the application
### Running with Flask built-in web server
1. Start the app and web server from command line:```./skein_run.py```
2. Access the application by the address *http://localhost:5000*

### Running with Apache mod_wsgi
1. [Set up](http://flask.pocoo.org/docs/0.11/deploying/mod_wsgi/) Apache mod_wsgi
2. Use `skein.wsgi` as a wsgi script in Apache config's `WSGIScriptAlias` variable

## Elasticsearch document structure
### Page object
Page documents located in `book-<i>` index, `pages` type. And has the following structure (example):
```json
{"_index":"book-1","_type":"pages","_id":"9","_score":1.0,
 "_source":{
      "page_no":  9,
      "chapter":  "Chapter 1",
      "section":  "",
      "subdivisions": "",
      "text": "Page text example"
}}
```

### Description object
Description documents located in `book-<i>` index, `description` type. And has the following structure (example):
```json
{"_index":"book-1","_type":"description","_id":"json","_score":1.0,
 "_source":{
    "index": "book-1",
    "name" : "The Last of the Mohicans",
    "author" : "James Fenimore Cooper",
    "country": "United States",
    "language": "English",
    "publisher": "H.C. Carey & I. Lea",
    "publication_date": "February 1826",
    "series" : "Leatherstocking Tales",
    "sequence" : 2,
    "genre" : "Historical novel"
}}
```
