import keras
import pickle
import gzip
import sys
import os
import cv2
# import thinning_algorithm
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from keras.models import Sequential
from keras.layers import InputLayer, Dense, Dropout
from keras.models import model_from_json
from keras.models import load_model
import json


MODEL_FILE_NAME = 'my_model.h5'


def load_image(imagename):
    img = cv2.imread(imagename, 0)
    img = np.asarray(img, dtype="float32")
    return img.reshape(784)


def loading_and_training():
    def load_database():
        train_x = []
        train_y = []
        for file in os.listdir(os.path.join("train_data", os.path.join("BlurredImages", "ResultImages"))):
            print(file)
            image = load_image(
                os.path.join("train_data", os.path.join("BlurredImages", os.path.join("ResultImages", file))))
            image = image.astype('float32')
            image /= 255
            train_x.append(image)
            train_y.append(int(file[0:2]))
        train_x = np.asarray(train_x)
        train_y = np.asarray(train_y)
        return train_x, train_y

    train_set = load_database()
    x_train = train_set[0]
    y_train = keras.utils.to_categorical(train_set[1], num_classes=74)

    model = keras.models.Sequential()
    model.add(InputLayer((784,)))
    model.add(Dropout(0.2))  # inaintea stratului pentru care vrem sa facem drop-out
    model.add(Dense(100, activation='relu'))
    model.add(Dense(74, activation='softmax'))
    model.compile(optimizer=keras.optimizers.RMSprop(lr=0.005), loss='categorical_crossentropy', metrics=["accuracy"])
    model.fit(x_train, y_train, epochs=10, batch_size=100)

    return model


cyrillic_translit = {10: [u'\u0410', 'A'], 11: [u'\u0430', 'a'],
                     12: [u'\u0411', 'B'], 13: [u'\u0431', 'b'],
                     14: [u'\u0412', 'V'], 15: [u'\u0432', 'v'],
                     16: [u'\u0413', 'G'], 17: [u'\u0433', 'g'],
                     18: [u'\u0414', 'D'], 19: [u'\u0434', 'd'],
                     20: [u'\u0415', 'E'], 21: [u'\u0435', 'e'],
                     22: [u'\u0416', 'Zh'], 23: [u'\u0436', 'zh'],
                     24: [u'\u0417', 'Z'], 25: [u'\u0437', 'z'],
                     26: [u'\u0418', 'I'], 27: [u'\u0438', 'i'],
                     28: [u'\u0419', 'I'], 29: [u'\u0439', 'i'],
                     30: [u'\u041a', 'K'], 31: [u'\u043a', 'k'],
                     32: [u'\u041b', 'L'], 33: [u'\u043b', 'l'],
                     34: [u'\u041c', 'M'], 35: [u'\u043c', 'm'],
                     36: [u'\u041d', 'N'], 37: [u'\u043d', 'n'],
                     38: [u'\u041e', 'O'], 39: [u'\u043e', 'o'],
                     40: [u'\u041f', 'P'], 41: [u'\u043f', 'p'],
                     42: [u'\u0420', 'R'], 43: [u'\u0440', 'r'],
                     44: [u'\u0421', 'S'], 45: [u'\u0441', 's'],
                     46: [u'\u0422', 'T'], 47: [u'\u0442', 't'],
                     48: [u'\u0423', 'U'], 49: [u'\u0443', 'u'],
                     50: [u'\u0424', 'F'], 51: [u'\u0444', 'f'],
                     52: [u'\u0425', 'Kh'], 53: [u'\u0445', 'kh'],
                     54: [u'\u0426', 'Ts'], 55: [u'\u0446', 'ts'],
                     56: [u'\u0427', 'Ch'], 57: [u'\u0447', 'ch'],
                     58: [u'\u0428', 'Sh'], 59: [u'\u0448', 'sh'],
                     60: [u'\u0429', 'Shch'], 61: [u'\u0449', 'shch'],
                     62: [u'\u042a', '"'], 63: [u'\u044a', '"'],
                     64: [u'\u042b', 'Y'], 65: [u'\u044b', 'y'],
                     66: [u'\u042c', "'"], 67: [u'\u044c', "'"],
                     68: [u'\u042d', 'E'], 69: [u'\u044d', 'e'],
                     70: [u'\u042e', 'Iu'], 71: [u'\u044e', 'iu'],
                     72: [u'\u042f', 'Ia'], 73: [u'\u044f', 'ia']}


# pentru fiecare litera vom asocia un index (corespunzator pozitiei)
# este nevoie de normalizare -> Nu mai trebuie sa tinem cont de fonturile diferite/size-urile diferite
#                               deoarece toate vor avea in spate acelasi sablon ("schelet")

# normalizarea/rafinarea - > Zhang-Suen algorithm


def __encode_utf8(_string):
    if sys.version_info < (3, 0):
        return _string.encode('utf-8')
    else:
        return _string


def to_latin(number):
    latinized_chr = ''
    # If character is in dictionary, it means it's a cyrillic so let's transliterate that character.
    if number in cyrillic_translit.keys():
        # Transliterate current character.
        latinized_chr += cyrillic_translit[number][1]

        # If character is not in character transliteration dictionary,
        # it is most likely a number or a special character so just keep it.
    else:
        latinized_chr += number
    # Return the transliterated string.
    return latinized_chr


def validate_network(rn_model, letters):
    # TODO: validate matrix dimenisons
    output = ""
    for letter in letters:
        test_set = np.asarray(letter)
        test_set = test_set.astype('float32')
        test_set /= 255
        result = rn_model.predict(test_set)
        idx = np.argmax(result)
        output += to_latin(idx)
    return len(output), output


if __name__ == '__main__':
    images = [r'train_data\BlurredImages\ResultImages\101-0-3.JPG',
              r'train_data\BlurredImages\ResultImages\111-0-3.JPG',
              r'train_data\BlurredImages\ResultImages\121-0-3.JPG',
              r'train_data\BlurredImages\ResultImages\131-0-3.JPG']
    pixels = [np.array(load_image(img) / 255).tolist() for img in images]
    json_input = json.dumps({'size': len(pixels), 'letters': pixels})
    with open('rn_input.json', 'w') as f:
        f.write(json_input)
    if os.path.exists(MODEL_FILE_NAME):
        rn_model = load_model(MODEL_FILE_NAME)
    else:
        rn_model = loading_and_training()
        rn_model.save(MODEL_FILE_NAME)
    '''
    while 1:
        imagename = input("Enter image name: ")
        if imagename == 'exit':
            break
        expectedoutput = input("Enter expected output: ")
        # thinning_algorithm.processImage(imagename)
        data_to_test = load_image(imagename)
        test_set = [data_to_test]
        test_set = np.asarray(test_set)
        test_set = test_set.astype('float32')
        test_set /= 255
        result = rn_model.predict(test_set)
        idx = np.argmax(result)
        print(to_latin(idx))
    # print("ExpectedOutput: "+to_latin(result))
    '''
