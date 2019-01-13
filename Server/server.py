from flask import Flask, render_template, request
from zipfile import ZipFile
import shutil
import base64
import zipfile
import os
import sys
import json
import requests
from os import path


# FLASK_APP=server.py flask run
# source gusPythonEnviroment/bin/activate
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/excel.html')
def excel():
    return render_template('excel.html')

@app.route('/serveste-mi-cererea', methods=['POST', 'GET'])
def servesteMiCererea():
    error = None
    text = []
    if request.method == 'POST':
        imagine = request.form.get("file", False)
        coordString = request.form.get('coordinates')
        coordString = coordString.replace('\"last_m_x\":', '').replace('\"last_m_y\":','').replace('\"gaz\":','').replace('\"heightx\":','').replace('[','').replace(']','').replace('\\','/')

        imagine = imagine[22:]

        fh = open("imageToSave.png", "wb")
        fh.write(base64.b64decode(imagine))
        fh.close()

        files = {'file' : open("imageToSave.png", "rb")}

    directoryOutputModule1 = "/home/augt/Public/AI Repo/AIA42018/Server/OutputForModule2"

    #delete stuffs------------------------------------------------------------------------------------------------------
    folder = directoryOutputModule1
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

    folder = "/home/augt/Public/AI Repo/AIA42018/Server/OutputForModule3/img"
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

    folder="/home/augt/Public/AI Repo/AIA42018/Server/OutputForModule3/json"
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

    #-------------------------------------------------------------------------------------------------------------------
    sys.path.append(path.abspath('../'))
    from Letter_Segmentation import letterSegmentation

    #Line Seg
    print(coordString)
    if len(coordString)>=9:
        token = requests.post('http://127.0.0.1:5000/upload/split',files=files, data = {'userid':'alex', 'coordinates': coordString}).content
    else:
        token = requests.post('http://127.0.0.1:5000/upload',files=files, data = {'userid':'alex'}).content

    token = token.decode("utf-8").split(' ')[3]
    print(token)
    archive = requests.get('http://127.0.0.1:5000/download/' + token.replace('"','').replace('}','')).content

    fh = open("ArchivesLine/arhiveLine.zip", "wb")
    fh.write(archive)
    fh.close()

    shutil.unpack_archive("ArchivesLine/arhiveLine.zip", extract_dir="/home/augt/Public/AI Repo/AIA42018/Server/OutputForModule2")


    # #Char Seg

    print('22222222222222222222222222222222222222')
    for filename in os.listdir(directoryOutputModule1):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            filepath = os.path.join(directoryOutputModule1, filename)
            letterSegmentation.letterSegm(filepath)

            continue
        else:
            continue



    # archive = ZipFile(lineArchive, 'r')
    # files = archive.namelist()
    # jsons = []
    # with ZipFile(lineArchive) as myzip:
    #     for file in files:
    #          with myzip.open(file) as myfile:
    #             jsons.append(requests.post('127.0.0.1:5001/charSplit', data = {'image':file.read()}).content)

    # #Char Rep
    # lineNewRoms = []
    # for jsonOne in jsons:
    #     jsonOneX = json.load(jsonOne)
    #     lineNewRoms.append(requests.post('127.0.0.1:5002/RN', data = {'json':jsonOneX}).content)

    # #Mapping
    # text = []
    # for lineNewRom in lineNewRoms:
    #     text.append(requests.post('127.0.0.1:5003/Mapping', data = {'text':lineNewRom}).content)
    return "abc";

if __name__ == '__main__':
    app.run(debug=True, port=8080)

    #char_seg accent verificat
    #RN ambiguitate cu in im
    #mapping cuvinte cu cratima verificat