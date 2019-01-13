from flask import Flask
import sys
from os import path
sys.path.append(path.abspath('../'))
from Char_Replacement import neural_network as nn
import os
import json
import keras
import json
from flask import request
from keras.models import load_model
from keras.layers import InputLayer, Dense, Dropout

app = Flask(__name__, static_folder='static')
IP = "0.0.0.0"
PORT = 5666
MODEL_FILE_NAME = 'my_model.h5'
rn_model = None


@app.route("/analyze_letters", methods=['POST'])  # json
def analyze_letters(json_data,count,result_path):
    #json_data = request.get_json(force=True)
    json_data = json.load(json_data)
    output_length, output = nn.validate_network(rn_model, json_data['letters'])
    json_output = json.dumps({'size': output_length, 'letters': output},ensure_ascii=False)
    with open(os.path.join(result_path,'rn_output_%s.json'%(count)), 'w',encoding="utf-8") as f:
        f.write(json_output)
    return json_output

def init():
    global rn_model
    if os.path.exists(os.path.join(app.static_folder, MODEL_FILE_NAME)):
        rn_model = keras.models.Sequential()
        rn_model.add(InputLayer((784,)))
        rn_model.add(Dropout(0.2))  # inaintea stratului pentru care vrem sa facem drop-out
        rn_model.add(Dense(250, activation='relu'))
        rn_model.add(Dense(113, activation='softmax'))
        rn_model.load_weights(os.path.join(app.static_folder, MODEL_FILE_NAME))
    else:
        rn_model = nn.loading_and_training()
        rn_model.save_weights(os.path.join(app.static_folder, MODEL_FILE_NAME))


if __name__ == '__main__':
    init()
    count =0
    # for path in os.listdir(r"D:\College_stuff\AN_3_Sem_1\IA\output\zona2"):
    #     count +=1
    #     with open(os.path.join(r"D:\College_stuff\AN_3_Sem_1\IA\output\zona2",path),"r") as file:
    #         analyze_letters(file,count)
    count = 0
    source_path = r"D:\College_stuff\AN_3_Sem_1\IA\output\zona1"
    result_path = "DESTINATIA"
    for img in os.listdir(source_path):
        with open(os.path.join(result_path,img), "r") as file:
            analyze_letters(file,count,result_path)
            count += 1
    # request_ip = "127.0.0.1" if IP else IP
    # print(f"Pentru a pune json-ul cu litere se face un POST pe {request_ip}:{PORT}")
    # app.run(debug=False, host=IP, port=PORT)
