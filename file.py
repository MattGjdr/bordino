import hashlib
import os
import datetime

from flask import request
from werkzeug.utils import secure_filename

from es import add_elastic


UPLOAD_FOLDER = '/home/matus/Documents/uploads'

TXT_EXTENSIONS = set(['txt'])
IMG_EXTENSIONS = set(['jpg'])

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
                	hash_img = hashlib.md5(datetime.datetime.now().strftime("%Y-%m-%d %H:%M").encode("utf-8")).hexdigest()
                	filename = secure_filename(file.filename)
                	file.save(os.path.join(UPLOAD_FOLDER, filename))
                	#todo, covnert image
                	os.system("cp "+os.path.join(UPLOAD_FOLDER, filename)+" "+ os.path.join(UPLOAD_FOLDER, hash_img+".jpg"))
                #otherwise parse it and upload to elastic
                if file and allowed_file_txt(file.filename):
                    filename = secure_filename(file.filename)
                    upload_to_elastic(file.read().decode("utf-8"), hash_img)
                return "Uploaded image"
        #todo, maybe return somathing more meaningful
        return "Somethings wrong"

def upload_to_elastic(file_data, hash_img=""):
	#todo, format
    add_elastic(file_data)