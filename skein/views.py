from flask import render_template, request, redirect, url_for, flash
from skein import app
from skein.forms import SForm
import requests
import json
import smtplib

@app.route("/", methods=['GET', 'POST'])
def index():
    form = SForm()
    print form.errors
    return render_template("search_form.html", form=form)

@app.route("/search", methods=['GET', 'POST'])
def search():
    form = SForm(request.form)
    if form.is_submitted():
        if not form.validate():
            flash("Fill in the search and email fields")
            return redirect(url_for('index'))
    
    r = requests.get("http://localhost:9200/_all/pages/_search?q=text:%s"
                        % form.search.data)

    es_pages = r.json()['hits']['hits']
    book_ids = { v['_index']:1 for v in es_pages }.keys()

    query = '{ "query" : { "constant_score" : { "filter" : { "terms" : { "_index" : [%s] } } } } }' % ', '.join( '"{}"'.format(v) for v in book_ids )
    
    r = requests.post('http://localhost:9200/_all/description/_search',
            data = query)
    
    es_books = { v['_index']:v for v in r.json()['hits']['hits'] }

    result = []
    for es_page in es_pages:
        print es_page['_source']
        index = es_page['_index']
        result.append({
            'title': es_books[index]['_source']['name'],
            'chapter': es_page['_source']['chapter'],
            'section': es_page['_source']['section'],
            'subdivisions': es_page['_source']['subdivisions'],
            'page_no': es_page['_source']['page_no']
        })
    
    body = "<p>Search: "+form.search.data+"</p>Result: <pre><code>"+json.dumps(result,indent=4)+"</code></pre>"
    try:
        send_email(form.email.data, body=body,subj="Your matching list")
    except:
        print "Unable to send the email"
    
    return "Data is being sent to "+form.email.data+body    

def send_email(address, body='', subj=''):
    message = """From: From Person <from@fromdomain.com>
    To: %s
    Subject: %s

    %s
    """ % (address, subj, body)

    s = smtplib.SMTP('localhost')
    s.sendmail('admin@mysite.com', address, message)
    s.quit()

    

