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
    
    es_pages = elastic_get(field='text', value=form.search.data, typ='pages')
    book_ids = { v['_index']:1 for v in es_pages}.keys()

    es_desc = { v['_index']:v for v in elastic_exact_match(field="_index",
                                            value='[%s]' % ', '.join( '"{}"'.format(v) for v in book_ids),
                                            typ='description') }
    result = []
    for es_page in es_pages:
        print es_page['_source']
        index = es_page['_index']
        result.append({
            'title': es_desc[index]['_source']['name'],
            'chapter': es_page['_source']['chapter'],
            'section': es_page['_source']['section'],
            'subdivisions': es_page['_source']['subdivisions'],
            'page_no': es_page['_source']['page_no']
        })
    
    keyword = form.search.data
    data = json.dumps(result,indent=4)
    sent_msg = send_email(form.email.data, 
                            body=render_template('result.html', keyword=keyword, data=data),
                            subject="Your matching list")
    
    return render_template("result.html", keyword=keyword, data=data, sent_msg=sent_msg )

def elastic_get(field, value, index='_all', typ='_all'):
    r = requests.get('http://localhost:9200/%s/%s/_search?q=%s:"%s"' % (index, typ, field, value) )
    return r.json()['hits']['hits']
    
def elastic_exact_match(field, value, index='_all', typ='_all'):   # find out about terms syntax in elasticsearch docs
    query = '{ "query" : { "constant_score" : { "filter" : { "terms" : {"%s":[%s]}}}}}' % (field, value)
    r = requests.post('http://localhost:9200/%s/%s/_search' % (index, typ), data = query)
    return r.json()['hits']['hits']
    
def send_email(recepient, body='', subject=''):
    gmail = 'skein.out@gmail.com'

    msg = "\r\n".join([
        "From: Testing Task %s" % gmail,
        "To: %s" % recepient,
        "Subject: %s" % subject,
         "Content-Type: text/html",
        "",
        body
    ])
    try:
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.set_debuglevel
        s.ehlo(); s.starttls(); s.ehlo()
        s.login(gmail, 'sk31n.t3st')
        s.sendmail(gmail, recepient, msg)
        s.quit()
        return "Data sent to " + recepient
    except:
        return "Was unable to email the result"


