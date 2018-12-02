from flask import Flask
import neural_network as nn
import os
import json
from keras.models import load_model


app = Flask(__name__, static_folder='static')
IP = "0.0.0.0"
PORT = 5666
MODEL_FILE_NAME = 'my_model.h5'
rn_model = None


@app.route("/analyze_letters", methods=['POST'])  # json
def analyze_letters(json_data):
    output_length, output = nn.validate_network(rn_model, json_data['letters'])
    json_output = json.dumps({'size': output_length, 'letters': output})
    with open('rn_output.json', 'w') as f:
        f.write(json_output)


def init():
    global rn_model
    if os.path.exists(os.path.join(app.static_folder, MODEL_FILE_NAME)):
        rn_model = load_model(os.path.join(app.static_folder, MODEL_FILE_NAME))
    else:
        rn_model = nn.loading_and_training()
        rn_model.save(os.path.join(app.static_folder, MODEL_FILE_NAME))


if __name__ == '__main__':
    init()
    request_ip = "127.0.0.1" if IP else IP
    print(f"Pentru a pune json-ul cu litere se face un POST pe {request_ip}:{PORT}")
    app.run(debug=False, host=IP, port=PORT)
