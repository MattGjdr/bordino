from flask import Flask, render_template

from flask_bootstrap import Bootstrap


app = Flask(__name__)
#bootstrap = Bootstrap(app)

@app.route('/')
def hello_world():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!',
            'link': '/'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!',
            'link': '/'
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
    return render_template('index.html', all_elements=elements, text_elements=elements, image_elements=elements)
    #return render_template('base.html', title='Home', user=user, posts=posts)
