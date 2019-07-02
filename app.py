import os
import json 

from flask import Flask, render_template
from flask import request, session, jsonify,send_from_directory, Response

from elasticsearch import Elasticsearch

from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

from es import add_elastic, delete_elastic, get_elastic, search_elastic, update_elastic
from file import upload_file, UPLOAD_FOLDER
from utils import elastic_to_html, html_to_elastic, elastic_to_html_all_filter

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
es = Elasticsearch()

#need for session
app.secret_key = 'any random string'

###CONFIG VARS####

all_elements = [
    {
        'name': 'title',
        'id': 'title'
    },
    {
        'name': 'date',
        'id': 'date'
    },
    {
        'name': 'location',
        'id': 'location'
    },
    {
        'name': 'content',
        'id': 'content'
    },
    {
        'name': 'comment',
        'id': 'comment'
    },
    {
        'name': 'references',
        'id': 'references'
    }
]

text_elements = all_elements
image_elements = all_elements

text_elements.append(
    {
        'name': 'author',
        'id': 'author'
    }
)
text_elements.append(
    {
        'name': 'chapter',
        'id': 'chapter'
    }
)
text_elements.append(
    {
        'name': 'latin',
        'id': 'latin'
    }
)

image_elements.append(
    {
        'name': 'material',
        'id': 'material'
    }
)

reasearch_keys = [
    'patronage','fabricating','restoring', 'worshiping', 'praying',
    'touching', 'kissing', 'burning light in front of images', 'offering precious gifts to images',
    'other veneration practices', 'describing', 'composing poems or inscriptions for material images', 'showing feelings',
    'blaming/showing scepticism/condemning', 'attacking/destryoing', 'miracles involving images'
]

#######################################################


@app.route('/', methods=["GET"])
def home():
    print(request.args)

 
    size = request.args.get("size", 1, int)
    start = request.args.get("start", 0, int)

    next=start+1

    if start>0:
        previous = start - 1
    else:
        previous = 0

    search_type = request.args.get("type", "all")

    admin = False
    if 'username' in session:
        admin = True
    
    results = search_elastic(request.args,search_type,start,size)
    res = results['hits']['hits']
    num_of_results = results['hits']['total']['value']
    if search_type == "all":
        res = elastic_to_html_all_filter(res)       

    # res = results['hits']['hits']
    # num_of_results = 0
    print(res)

    return render_template('index.html', 
        all_elements=all_elements, 
        text_elements=text_elements, 
        image_elements=image_elements, 
        reasearch_keys=reasearch_keys, 
        results=res, 
        num=num_of_results,
        admin=admin,
        next=next,
        previous=previous
    )


@app.route('/login', methods=["GET","POST"])
def login():
    
    if 'logout' in request.args:
        session.pop('username', None)

    #todo verification
    if 'username' in session:
        username = session['username']
        print(username)
        if username == "a":
            message = upload_file(request)
            return render_template('login.html', logged=True, message=message)


    logged = False
    if request.method == "POST":
        if request.form['uname'] == "a":
        #,request.form['psw']):
            logged = True
            session['username'] = request.form['uname']

    return render_template('login.html', logged=logged)


@app.route('/edit/<id>', methods=["GET"])
def edit(id):
    #todo verification
    if 'username' in session:
        results = get_elastic(id)
        
        results = elastic_to_html(results)

        return render_template('edit.html', id=id, elements=results['_source'], disabled="")


@app.route('/show/<id>', methods=["GET"])
def show(id):
    #todo verification
    results = get_elastic(id)

    results = elastic_to_html(results)

    return render_template('edit.html', id=id, elements=results['_source'], disabled="disabled")


@app.route('/download/<type>/<id>', methods=["GET"])
def download(id, type):
    #todo verification
    if (type == "txt"):
        results = get_elastic(id)
        #obsah suboru
        generator = json.dumps(results)
        return Response(generator, mimetype="text/plain", headers={"Content-Disposition": "attachment;filename=test.txt"})
    elif (type == "img"):
        results = get_elastic(id)
        #obsah suboru
        generator = json.dumps(results)
        return Response(generator, mimetype="text/plain", headers={"Content-Disposition": "attachment;filename=test.jpg"})


@app.route('/delete/<id>', methods=["GET"])
def delete(id):
    #todo verification
    if 'username' in session:
        delete_elastic(id)
    return redirect('/')


@app.route('/update/<id>', methods=["GET"])
def upload(id):
    #todo verification
    if 'username' in session:
        args = html_to_elastic(request.args.to_dict())
        update_elastic(id, args)
    return redirect('/edit/'+id)

