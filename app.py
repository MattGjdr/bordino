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
    return render_template('index.html', all_elements=all_elements, text_elements=elements, image_elements=elements, reaserch_keys=reaserch_keys)
    #return render_template('base.html', title='Home', user=user, posts=posts)
