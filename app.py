import os
import json 

from flask import Flask, render_template
from flask import request, session, jsonify,send_from_directory, Response

from elasticsearch import Elasticsearch

from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

from es import add_elastic, delete_elastic, get_elastic, search_elastic, update_elastic

#code
UPLOAD_FOLDER = '/home/matus/Documents/uploads'
TXT_EXTENSIONS = set(['txt'])
IMG_EXTENSIONS = set(['jpg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
es = Elasticsearch()

#need for session
app.secret_key = 'any random string'


def allowed_file_txt(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in TXT_EXTENSIONS

def allowed_file_img(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in IMG_EXTENSIONS


def upload_file(request):
    if request.method == 'POST':
        # array of files, 2 to be precise
        if 'file[]' not in request.files and 'file' not in request.files:
            return "No file part"

        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return "No selected part"
            if file and allowed_file_txt(file.filename):
                filename = secure_filename(file.filename)
                upload_to_elastic(file.read().decode("utf-8"))
            return "Uploaded text"
        else:
            list_of_files = request.files.getlist("file[]")
            #list of files to loop through
            for file in list_of_files:
                if file.filename == '':
                    return "No selected part"
                #if file is image, save it 
                if file and allowed_file_img(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                #otherwise parse it and upload to elastic
                if file and allowed_file_txt(file.filename):
                    filename = secure_filename(file.filename)
                    upload_to_elastic(file.read().decode("utf-8"))
                return "Uploaded image"
        #todo, maybe return somathing more meaningful
        return "Somethings wrong"


def upload_to_elastic(file_data):
    add_elastic(file_data)

def parse_date_material_keys(res):

    # res["_source"]["date"] = res["_source"]["date"]
    # del res["_source"]["path"]

    if (type(res["_source"]["material"])==list):
        res["_source"]["material"] = ', '.join(res["_source"]["material"])
    if (type(res["_source"]["keys"])==list):
        res["_source"]["keys"] = ', '.join(res["_source"]["keys"])
    if (type(res["_source"]["references.studies"])==list):
        res["_source"]["studies"] = '\n\n'.join(res["_source"]["references.studies"])

    res["_source"]["translation"] = res["_source"]["references.translation"]
    res["_source"]["edition"] = res["_source"]["references.edition"]

    del res["_source"]["references.edition"]
    del res["_source"]["references.translation"]
    del res["_source"]["references.studies"]
    
    return res

def glue_date_material_keys(args):
    
    #res["_source"]["date"] = res["_source"]["date"]
    #path
    
    args['material'] = args['material'].split(',')
    args['references.studies'] = args['studies'].split('\n\n')
    args['references.translation'] = args['translation']
    args['references.edition'] = args['edition']
    args['keys'] = args['keys'].split(',')
    
    return args



@app.route('/', methods=["GET"])
def home():
    print(request.args)

    admin = False
    if 'username' in session:
        admin = True

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

    results = search_elastic(request.args)

    reasearch_keys = [
    'patronage','fabricating','restoring', 'worshiping', 'praying',
    'touching', 'kissing', 'burning light in front of images', 'offering precious gifts to images',
    'other veneration practices', 'describing', 'composing poems or inscriptions for material images', 'showing feelings',
    'blaming/showing scepticism/condemning', 'attacking/destryoing', 'miracles involving images'
    ]
    return render_template('index.html', all_elements=all_elements, text_elements=text_elements, image_elements=image_elements, reasearch_keys=reasearch_keys, results=results, admin=admin)


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
        
        results = parse_date_material_keys(results)

        return render_template('edit.html', id=id, elements=results['_source'], disabled="")


@app.route('/show/<id>', methods=["GET"])
def show(id):
    #todo verification
    results = get_elastic(id)

    results = parse_date_material_keys(results)

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
        args = glue_date_material_keys(request.args.to_dict())
        update_elastic(id, args)
    return redirect('/edit/'+id)

