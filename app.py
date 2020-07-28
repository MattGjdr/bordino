import os
import json 

from flask import Flask, render_template
from flask import request, session, jsonify,send_from_directory, Response, send_file

from elasticsearch import Elasticsearch

from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

from es import add_elastic, delete_elastic, get_elastic, search_elastic, update_elastic
from file import upload_file, UPLOAD_FOLDER, STATIC_IMAGE_FOLDER
from utils import elastic_to_html, html_to_elastic, elastic_to_html_all_filter, check_elastic_res, append_date_to_res

from format import write_xml, read_xml

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_IMAGE_FOLDER'] = STATIC_IMAGE_FOLDER

es = Elasticsearch()

#need for session
app.secret_key = 'any random string'

###CONFIG VARS####

all_elements = [
    {
        'name': 'Title of work',
        'id': 'title',
        'placeholder': 'text'
    },
    {
        'name': 'Date',
        'id': 'date',
        'placeholder': 'write years from-to, (eg. 100-120)'
    },
    {
        'name': 'Location',
        'id': 'location',
        'placeholder': 'text'
    },
    {
        'name': 'Content of work',
        'id': 'content',
        'placeholder': 'text'
    },
    {
        'name': 'Comment about work',
        'id': 'comment',
        'placeholder': 'text'
    },
    {
        'name': 'Bibliographic references',
        'id': 'references',
        'placeholder': 'text'
    },
    {
        'name': 'Type of work',
        'id': 'type',
        'placeholder': 'text'
    }
]


text_elements = all_elements.copy()
image_elements = all_elements.copy()

text_elements.append(
    {
        'name': 'Author of work',
        'id': 'author',
        'placeholder': 'text'
    }
)
text_elements.append(
    {
        'name': 'Chapter of work',
        'id': 'chapter',
        'placeholder': 'text'
    }
)
text_elements.append(
    {
        'name': 'Latin text',
        'id': 'latin',
        'placeholder': 'text'
    }
)

# reasearch_keys = [
#     'patronage','fabricating','restoring', 'worshiping', 'praying',
#     'touching', 'kissing', 'burning light in front of images', 'offering precious gifts to images',
#     'other veneration practices', 'describing', 'composing poems or inscriptions for material images', 'showing feelings',
#     'blaming/showing scepticism/condemning', 'attacking/destryoing', 'miracles involving images'
# ]

f = open('researchkeys.txt', 'r') 
Lines = f.readlines() 
reasearch_keys = []
# Strips the newline character 
for line in Lines: 
    reasearch_keys.append(line.strip()) 
#######################################################


"""
    Function GET args from query and search in elasticsearch for relevant results
"""
@app.route('/', methods=["GET"])
def home():
    print(request.args)

    num_show_results = 2
    size = request.args.get("size", num_show_results, int)
    start = request.args.get("start", 0, int)

    next=start+num_show_results

    if start>(num_show_results-1):
        previous = start-num_show_results
    else:
        previous = 0

    search_type = request.args.get("t", "all")

    admin = False
    if 'username' in session:
        admin = True
    
    results, check_date = search_elastic(request.args,search_type,start,size)

    try:
        res = results['hits']['hits']
        num_of_results = results['hits']['total']['value']

        if search_type == "all":
            res = elastic_to_html_all_filter(res) 
        else:
            if check_date:
                res = append_date_to_res(res)
            if check_elastic_res(res):
                res = elastic_to_html_all_filter(res)
    except:
        res = []
        num_of_results = 0      

    # res = results['hits']['hits']
    # num_of_results = 0
    print("-----------------------")
    print(res)
    print("-----------------------")
    return render_template('index.html', 
        all_elements=all_elements, 
        text_elements=text_elements, 
        image_elements=image_elements, 
        reasearch_keys=reasearch_keys, 
        results=res, 
        num=num_of_results,
        admin=admin,
        next=next,
        previous=previous,
        num_show_results=num_show_results
    )

"""
    Function create and release season and check username password
"""
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
    if request.method == "POST" and request.form['uname'] == "a" and request.form['psw'] == "a":
        #,request.form['psw']):
            logged = True
            session['username'] = request.form['uname']

    return render_template('login.html', logged=logged)

"""
    Function show info from elasticsearch based on ID, which can be edited
"""
@app.route('/edit/<id>', methods=["GET"])
def edit(id):
    #todo verification
    if 'username' in session:
        results = get_elastic(id)
        
        results, img = elastic_to_html(results)

        xml = write_xml(results['_source'])

        return render_template('edit.html', id=id, elements=results['_source'], xml=xml, disabled="", img=img)

"""
    Function show info from elasticsearch based on ID
"""
@app.route('/show/<id>', methods=["GET"])
def show(id):
    #todo verification
    results = get_elastic(id)

    results, img = elastic_to_html(results, "show")

    xml = "" #write_xml(results['_source'])

    return render_template('edit.html', 
        text_elements=text_elements, 
        image_elements=image_elements, 
        id=id, 
        elements=results['_source'], 
        xml=xml, disabled="disabled", 
        img=img)

"""
    Function create file for downloading, it could be image or text
"""
@app.route('/download/<type>/<id>', methods=["GET"])
def download(id, type):
    #todo verification
    if (type == "txt"):
        return download_txt(id,type)

    
    elif (type == "img"):
        return download_img(id,type)


"""
    Function create text file for downloading
"""
def download_txt(id,type):
    results = get_elastic(id)
    #obsah suboru
    xml = write_xml(results['_source'])
    generator = xml
    return Response(generator, mimetype="text/plain", headers={"Content-Disposition": "attachment;filename="+id+".xml"})

"""
    Function create zip file for downloading
"""
def download_img(id,type):
    results = get_elastic(id)
    hashes_img = results['_source']['path']
    ref_img = results['_source']['references.photo']
    #obsah suboru
    for idx, img in enumerate(hashes_img):
        hashes_img[idx] = os.path.join(UPLOAD_FOLDER, img+".jpg")

    #obsah ref
    refs = ""
    for idx, ref in enumerate(ref_img):
        refs += ref+"\n"

    str_images = " ".join(hashes_img)
    zip_path = os.path.join(UPLOAD_FOLDER, id+".zip")
    ref_path = os.path.join(UPLOAD_FOLDER, "references_"+id+".txt")
    os.system("echo \""+refs+"\" > "+ref_path)
    os.system("zip -j "+zip_path+" "+str_images+" "+ref_path)
    
    return send_file(zip_path, as_attachment=True, cache_timeout=0)

"""
    Function delete info from elasticsearch based on ID
"""
@app.route('/delete/<id>', methods=["GET"])
def delete(id):
    #todo verification
    if 'username' in session:
        results = get_elastic(id)
        if 'path' in results['_source']:
            hashes_img = results['_source']['path']
            for idx, img in enumerate(hashes_img):
                print(os.path.join(STATIC_IMAGE_FOLDER, img+".jpg"))
                print(os.path.join(UPLOAD_FOLDER, img+".jpg"))
                os.system("rm "+os.path.join(STATIC_IMAGE_FOLDER, img+".jpg"))
                os.system("rm "+os.path.join(UPLOAD_FOLDER, img+".jpg"))

        delete_elastic(id)
    return redirect('/')

"""
    Function update info from elasticsearch based on ID
"""
@app.route('/update/<type>/<id>', methods=["GET"])
def upload(type, id):
    #todo verification
    if 'username' in session:
        parsed_xml, _ = read_xml(request.args.to_dict()['xml'], type)
        update_elastic(id, parsed_xml)
  
    return redirect('/edit/'+id)

"""
    Function show about html page
"""
@app.route('/about', methods=["GET"])
def about():
    return render_template('about.html')

