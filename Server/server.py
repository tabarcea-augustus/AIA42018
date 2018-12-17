from flask import Flask, render_template, request
from zipfile import ZipFile
import shutil

import json
import requests

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

    # #Line Seg
    # token = requests.post('127.0.0.1:5000/upload/split', data = {'file':imagine, 'coordinates': coordString}).content
    # lineArchive = request.get('https://AI/LS/input')

    # #Char Seg
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
    return text;

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

    #char_seg accent verificat
    #RN ambiguitate cu in im
    #mapping cuvinte cu cratima verificat