from flask import Flask, render_template
from flask import request, session


app = Flask(__name__)
app.secret_key = 'any random string'
#bootstrap = Bootstrap(app)

@app.route('/', methods=["GET"])
def home():
    admin = False
    if 'username' in session:
        admin = True

    results = [
        {
            'image': '/static/photo.jpeg',
            'data': {
                'title': 'blaabla',
                'this': 'rararar',
                'author': 'krakra'
            }
        },
        {
            'image': '/static/photo.jpeg',
            'data': {
                'title': 'blaabla',
                'this': 'rararar',
                'author': 'krakra'
            }
        }
    ]

    elements = [
        {
            'name': 'name'
        },
        {
            'name': 'fame'
        }
    ]

    all_elements = [
        {
            'time': 'time'
        },
        {
            'text': 'text'
        }
    ]

    reaserch_keys = [
    'patronage','fabricating','restoring', 'worshiping', 'praying',
    'touching', 'kissing', 'burning light in front of images', 'offering precious gifts to images',
    'other veneration practices', 'describing', 'composing poems or inscriptions for material images', 'showing feelings',
    'blaming/showing scepticism/condemning', 'attacking/destryoing', 'miracles involving images'
    ]
    return render_template('index.html', all_elements=all_elements, text_elements=elements, image_elements=elements, reaserch_keys=reaserch_keys, results=results, admin=admin)


@app.route('/login', methods=["GET","POST"])
def login():
    
    if 'logout' in request.args:
        session.pop('username', None)

    if 'username' in session:
        username = session['username']
        print(username)
        if username == "a":
            return render_template('login.html', logged=True)


    logged = False
    if request.method == "POST":
        if request.form['uname'] == "a":
        #,request.form['psw']):
            logged = True
            session['username'] = request.form['uname']
            

    return render_template('login.html', logged=logged)