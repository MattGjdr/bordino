import hashlib
import os
import datetime

from flask import request
from werkzeug.utils import secure_filename

from es import add_elastic

from format import read_xml

UPLOAD_FOLDER = '/home/matus/Documents/uploads'
STATIC_IMAGE_FOLDER = '/home/matus/Documents/bordino/static/img'

TXT_EXTENSIONS = set(['xml'])
IMG_EXTENSIONS = set(['jpg'])

"""
    Function check text file name
"""
def allowed_file_txt(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in TXT_EXTENSIONS
"""
    Function check image file name
"""
def allowed_file_img(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in IMG_EXTENSIONS

"""
    Function get request query and based whether it is list or just string, it decides what is going to be uploaded
    if list then image and text is uploaded to elasticsearch
    if string then text is uploaded to elasticsearch
"""
def upload_file(request):
    img_txt = False
    txt_img = False
    txt = False
    response = False

    if request.method == 'POST':
        # array of files, 2 to be precise
        if 'file[]' not in request.files and 'file' not in request.files:
            return "Upload failed! (no files)"

        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return "Upload failed! (no files)"
            if file and allowed_file_txt(file.filename):
                filename = secure_filename(file.filename)
                txt = True
                response = upload_to_elastic(file.read().decode("utf-8"))
        else:
            list_of_files = request.files.getlist("file[]")
            #list of files to loop through
            if len(list_of_files) != 2:
            	return "Upload failed! (too many files)"

            for file in list_of_files:
                hash_img = hashlib.md5(datetime.datetime.now().strftime("%Y-%m-%d %H:%M").encode("utf-8")).hexdigest()
                if file.filename == '':
                    return "Upload failed! (no files)"
                #if file is image, save it 
                if file and allowed_file_img(file.filename):
                	img_txt = True
                	filename = secure_filename(file.filename)
                	file.save(os.path.join(UPLOAD_FOLDER, filename))           
                	os.system("cp "+os.path.join(UPLOAD_FOLDER, filename)+" "+ os.path.join(UPLOAD_FOLDER, hash_img+".jpg"))
                	#todo, convert image
                	os.system("cp "+os.path.join(UPLOAD_FOLDER, hash_img+".jpg")+" "+ os.path.join(STATIC_IMAGE_FOLDER, hash_img+".jpg &"))

                #otherwise parse it and upload to elastic
                if file and allowed_file_txt(file.filename):
                    txt_img = True
                    filename = secure_filename(file.filename)
                    response = upload_to_elastic(file.read().decode("utf-8"), hash_img)


        if response:
    	    if txt:
    		    return "Uploaded of text succesfull"
    	    elif img_txt and txt_img:
    		    return "Uploaded of text and image succesfull"
    	    else:
    		    return "Upload failed! (wrong files uploaded)"
        else:
    	    #todo, maybe return somathing more meaningful
    	    return "Upload failed! (uploading to server failed)"

"""
    Function read data from xml and send it to elasticsearch function which upload it
"""
def upload_to_elastic(file_data, hash_img=""):
    if (hash_img == ""):
        new_item = read_xml(file_data, "txt")
    else:
        new_item = read_xml(file_data, "img", hash_img)

    if (new_item == False):
        return False
    else:
        add_elastic(new_item)
        return True

