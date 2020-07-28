import hashlib
import os
import datetime
import random

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
        Function upload txt to elastic
"""
def upload_txt(xml):
    filename = secure_filename(xml[0].filename)
    return upload_to_elastic(xml[0].read().decode("utf-8"))

"""
        Function upload jpgs and txt to elastic
"""
def upload_img(xml, list_of_jpgs):
    img_hashes = list()
    for image in list_of_jpgs:
        hash_img = hashlib.md5(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%6").encode("utf-8")+str(random.randint(1,9999)).encode("utf-8")+image.filename.encode("utf-8")).hexdigest()
        if image and allowed_file_img(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(UPLOAD_FOLDER, filename))
            os.system("cp "+os.path.join(UPLOAD_FOLDER, filename)+" "+ os.path.join(UPLOAD_FOLDER, hash_img+".jpg"))
            #todo, convert image
            os.system("cp "+os.path.join(UPLOAD_FOLDER, hash_img+".jpg")+" "+ os.path.join(STATIC_IMAGE_FOLDER, hash_img+".jpg &"))
            img_hashes.append(hash_img)

    if xml[0] and allowed_file_txt(xml[0].filename):
        filename = secure_filename(xml[0].filename )
        return upload_to_elastic(xml[0].read().decode("utf-8"), img_hashes)

    return False, "Image upload failed"

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
    msg = "Files missing"
    if request.method != 'POST':
        return

    print(request.files)
    list_of_jpgs = request.files.getlist("jpgs[]")
    xml = request.files.getlist("xml")
    print(list_of_jpgs)

    if list_of_jpgs[0].filename == '' and xml[0].filename != '' and xml[0] and allowed_file_txt(xml[0].filename):
        txt = True
        response, msg = upload_txt(xml)
        

    if list_of_jpgs[0].filename != '' and xml[0].filename != '':
        img = True
        response, msg = upload_img(xml, list_of_jpgs)
        
    if response and txt:
        return "Uploaded of text succesfull"
    elif response and img:
        return "Uploaded of text and image succesfull"
    elif response:
            return "Unexpected behaviour, try again, perhaps something with wrong files uploaded"
    else:
        #todo, maybe return somathing more meaningful
        return "Upload failed: "+msg

"""
        Function read data from xml and send it to elasticsearch function which upload it
"""
def upload_to_elastic(file_data, hash_img=""):
    if (hash_img == ""):
        new_item, msg = read_xml(file_data, "txt")
    else:
        new_item, msg = read_xml(file_data, "img", hash_img)

    if (new_item == False):
        return False, msg
    else:
        add_elastic(new_item)
        return True, ""