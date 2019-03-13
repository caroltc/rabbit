#!/usr/bin/python
#-*-coding:utf-8-*-

from flask import Flask
from flask import render_template
from flask import request
from werkzeug import secure_filename
import os,sys
import ConfigParser
app = Flask(__name__)

@app.route('/')
def index():
    cf = ConfigParser.ConfigParser()
    cf.read("config.ini")
    read_folder = cf.get("common", "read_folder")
    fileHandle = FileHandle()
    fileHandle.get_paths(read_folder)
    fileHandle.get_compress_files(read_folder)
    return render_template('upload.html', paths = fileHandle.dirs, rar_files = fileHandle.rar_files, zip_files = fileHandle.zip_files)

@app.route('/doupload', methods=['POST'])
def doupload():
    upload_path = request.form['file_path']
    f = request.files['file']
    f.save(upload_path+'/'+f.filename.replace(' ',''))
    return 'upload success!'

@app.route('/uncompress', methods=['POST'])
def uncompress():
    file_path = request.form['file_path']
    rar_file = request.form['rar_file']
    zip_file = request.form['zip_file']
    if rar_file:
        os.system('./uncompress_rar.sh '+rar_file+' '+file_path)
    elif zip_file:
        os.system('./uncompress_zip.sh '+zip_file+' '+file_path)
    return 'success!'

@app.route('/mkdir', methods=['POST'])
def mkdir():
    file_path = request.form['file_path']
    dir_name = request.form['dir_name']
    if dir_name:
        os.mkdir(file_path + '/' + dir_name)
    return 'success!'


class FileHandle:
    def __init__(self):
        self.dirs = []
        self.rar_files = []
        self.zip_files = []

    def get_paths(self, read_folder):
        for (root,dirs,files) in os.walk(read_folder) :
            for dirname in dirs:
                self.dirs.append(root+'/'+str(dirname))

    def get_compress_files(self, read_folder):
        for (root,dirs,files) in os.walk(read_folder) :
            for file_name in files:
                file=os.path.splitext(root+'/'+str(file_name))
                filename,type=file
                if type.lower() == '.rar':
                    self.rar_files.append(root+'/'+str(file_name))
                elif type.lower() == '.zip':
                    self.zip_files.append(root+'/'+str(file_name))

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8') 
    app.run(debug=True)