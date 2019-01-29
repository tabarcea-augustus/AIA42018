from flask import Flask
import neural_network as nn
import os
import json
import keras
import json
from flask import request
from keras.models import load_model
from keras.layers import InputLayer, Dense, Dropout
import shutil
import re

app = Flask(__name__, static_folder='static')
IP = "0.0.0.0"
PORT = 5666
MODEL_FILE_NAME = 'my_model.h5'
rn_model = None


@app.route("/analyze_letters", methods=['POST'])  # json
def analyze_letters(json_data, count, result_path):
    # json_data = request.get_json(force=True)
    json_data = json.load(json_data)
    output_length, output = nn.validate_network(rn_model, json_data['letters'])
    json_output = json.dumps({'size': output_length, 'letters': output}, ensure_ascii=False)
    with open(os.path.join(result_path, 'rn_output_%s.json' % (count)), 'w', encoding="utf-8") as f:
        f.write(json_output)
    return json_output


def init():
    global rn_model
    if os.path.exists(os.path.join(app.static_folder, MODEL_FILE_NAME)):
        rn_model = keras.models.Sequential()
        rn_model.add(InputLayer((784,)))
        rn_model.add(Dropout(0.2))  # inaintea stratului pentru care vrem sa facem drop-out
        rn_model.add(Dense(200, activation='relu'))
        rn_model.add(Dense(99, activation='softmax'))
        rn_model.load_weights(os.path.join(app.static_folder, MODEL_FILE_NAME))
    else:
        rn_model = nn.loading_and_training()
        rn_model.save_weights(os.path.join(app.static_folder, MODEL_FILE_NAME))


if __name__ == '__main__':
    # Antrename: WHAT_TO_DO -> 1
    #   reateua este antrenata pe folderul_training_data
    #       pentru a adauga noi poze, trebuie puse cu id-ul din retea (pentru litera) si _ si un numar oarecare (imaginea trebuie sa fie 28x28)
    # Testare:
    #   Input: Se va face testarea pe jsoane-le din source_path (declarata mai jos)
    #   Output: Va fi pus in result_path declarat mai jos
    save_weights_location = os.path.join('static', MODEL_FILE_NAME)
    WHAT_TO_DO = 2  # TODO: 1-TRAIN AGAIN, 2-just TEST
    if WHAT_TO_DO is 1:
        if os.path.exists(save_weights_location):
            os.remove(save_weights_location)
    init()
    count = 0
    source_path = "test_data"
    c_dir = os.getcwd()
    result_path = "result_data"
    for img in os.listdir(source_path):
        c_img = os.path.join(c_dir, source_path, img)
        with open(os.path.join(result_path, c_img), "r") as file:
            analyze_letters(file, count, result_path)
            count += 1
    # print(count)
    # # request_ip = "127.0.0.1" if IP else IP
    # # print(f"Pentru a pune json-ul cu litere se face un POST pe {request_ip}:{PORT}")
    # # app.run(debug=False, host=IP, port=PORT)
