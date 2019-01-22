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

    directoryOutputModule1 = "./OutputForModule2"

    #delete stuffs------------------------------------------------------------------------------------------------------
    for the_file in os.listdir(directoryOutputModule1):
        file_path = os.path.join(directoryOutputModule1, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

    directoryOutputModule2_img = "./OutputForModule3/img"
    for the_file in os.listdir(directoryOutputModule2_img):
        file_path = os.path.join(directoryOutputModule2_img, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

    directoryOutputModule2_json="./OutputForModule3/json"
    for the_file in os.listdir(directoryOutputModule2_json):
        file_path = os.path.join(directoryOutputModule2_json, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

    directoryOutputModule3 = "./OutputForModule4"
    for the_file in os.listdir(directoryOutputModule3):
        file_path = os.path.join(directoryOutputModule3, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

    #-------------------------------------------------------------------------------------------------------------------
    sys.path.append(path.abspath('../'))
    from Letter_Segmentation import letterSegmentation as module2
    from Char_Replacement import server as module3
    from Mapping import mapping_module as module4

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
            module2.letterSegm(filepath)

            continue
        else:
            continue

    #Char Rep
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    # for filename in os.listdir(directoryOutputModule2_json):
    #     if filename.endswith(".json"):
    #         filepath = os.path.join(directoryOutputModule2_json, filename)
    #         print(filepath)
    #         files = {'file': open(filepath, "r")}
    #         result = requests.post('http://127.0.0.1:5666/analyze_letters', files=files, data={}).content
    #         print(token)
    #         break
    module3.main()
    print('DONE')


    # #Mapping
    # text = []
    # for lineNewRom in lineNewRoms:
    #     text.append(requests.post('127.0.0.1:5003/Mapping', data = {'text':lineNewRom}).content)
    result = ""
    module4ListResult = []
    for filename in os.listdir(directoryOutputModule3):
        if filename.endswith(".json"):
            filepath = os.path.join(directoryOutputModule3, filename)
            print("MODULE 4: " ,filepath)
            module4ListResult = module4.map_words(filepath)
            for cuvant in module4ListResult:
                result += " "
                result += cuvant

    print(result)
    return result

if __name__ == '__main__':
    app.run(debug=True, port=8080, ssl_context=('cert.pem', 'key.pem'))

    #char_seg accent verificat
    #RN ambiguitate cu in im
    #mapping cuvinte cu cratima verificat