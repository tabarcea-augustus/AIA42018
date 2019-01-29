import os
import sys
import json
import cv2
import keras
# import thinning_algorithm
import numpy as np
from keras.layers import InputLayer, Dense, Dropout

MODEL_FILE_NAME = 'my_model.h5'


def load_image(imagename):
    img = cv2.imread(imagename, 0)
    img = np.asarray(img, dtype="float32")
    img = img.reshape(784)
    return img


def transform_images_to_json(input_folder, output_location_file):
    train_x = []
    for file in os.listdir(input_folder):
        c_file = os.path.join(input_folder, file)
        image = load_image(c_file)
        image = image.astype('float32')
        image /= 255
        train_x.append(image.tolist())
    c_len = train_x
    json_output = json.dumps({'size': c_len, 'letters': train_x}, ensure_ascii=False)
    with open(output_location_file, 'w') as f:
        f.write(json_output)


def loading_and_training():
    def load_database():
        train_x = []
        train_y = []
        for file in os.listdir("training_data"):
            image = load_image(os.path.join("training_data", file))
            image = image.astype('float32')
            image /= 255
            train_x.append(image)
            train_y.append(int(file.split('_')[0]))
        train_x = np.asarray(train_x)
        train_y = np.asarray(train_y)
        return train_x, train_y

    train_set = load_database()
    x_train = train_set[0]
    y_train = keras.utils.to_categorical(train_set[1], num_classes=99)

    model = keras.models.Sequential()
    model.add(InputLayer((784,)))
    model.add(Dropout(0.2))  # inaintea stratului pentru care vrem sa facem drop-out
    model.add(Dense(200, activation='relu'))
    model.add(Dense(99, activation='softmax'))
    model.compile(optimizer=keras.optimizers.RMSprop(lr=0.005), loss='categorical_crossentropy', metrics=["accuracy"])
    model.fit(x_train, y_train, epochs=15, batch_size=1000)

    return model


# de sters valoarea din dict. De lasat numai a doua val (vezi 10,11)
# de uitat la fiecare litera si te pus corespondentul in latina (uitandu-te la fiecare imagine)
# vezi link https://www.loc.gov/catdir/cpso/romanization/romanian.pdf?fbclid=IwAR25XPRClR-Mjf1xjw7k74lavdacloR0xm8MWvhytk81NpeaeaV_dqabEXM
# de refacut baza de date (de rulat scriptul de blur in noul folder Base-Data)
# reantrenat reteaua
cyrillic_translit = {0: '0', 1: '1',
                     2: '2', 3: '3',
                     4: '4', 5: '5',
                     6: '6', 7: '7',
                     8: '8', 9: '9',
                     10: 'A', 11: 'a',
                     12: 'B', 13: 'b',
                     14: 'V', 15: 'v',
                     16: 'G', 17: 'g',
                     18: 'D', 19: 'd',
                     20: 'E', 21: 'e',
                     22: 'J', 23: 'j',
                     24: 'Zh', 25: 'zh',
                     26: 'Z', 27: 'z',
                     28: 'I', 29: 'i',
                     30: 'Ih', 31: 'ih',
                     32: 'Ih', 33: 'ih',
                     34: 'C', 35: 'c',
                     36: 'L', 37: 'l',
                     38: 'M', 39: 'm',
                     40: 'N', 41: 'n',
                     42: 'O', 43: 'o',
                     44: 'P', 45: 'p',
                     46: 'R', 47: 'r',
                     48: 'S', 49: 's',
                     50: 't', 51: 't',
                     52: 'U', 53: 'u',
                     54: 'F', 55: 'f',
                     56: 'H', 57: 'h',
                     58: 'Oh', 59: 'oh',
                     60: 'Ț', 61: 'ț',
                     62: 'Ch', 63: 'ch',
                     64: 'Ș', 65: 'ș',
                     66: "Șt", 67: "șt",
                     68: 'Y', 69: 'y',
                     70: "'", 71: "'",
                     72: 'Ea', 73: 'ea',
                     74: 'Iu', 75: 'iu',
                     76: 'Ia', 77: 'ia',
                     78: 'Ie', 79: 'ie',
                     80: 'Iha', 81: 'Iha',
                     82: 'Â', 83: 'â',
                     84: 'X', 85: 'x',
                     86: 'Ps', 87: 'ps',
                     88: 'Th', 89: 'th',
                     90: 'Yh', 91: 'yh',
                     92: 'Î', 93: 'î',
                     94: 'Gh', 95: 'gh',
                     96: ' ',
                     97: 'Ă', 98: 'ă'}


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
        latinized_chr += cyrillic_translit[number]
    return latinized_chr


def is_space(letter):
    return sum([1 for lx in letter if lx == 1.0]) < 10


def validate_network(rn_model, letters):
    # TODO: validate matrix dimenisons
    output = ""
    for letter in letters:
        if is_space(letter):
            output += ' '
            continue
        test_set = np.array(letter)
        test_set = [test_set.reshape((784,))]
        test_set = np.asarray(test_set)
        test_set = test_set.astype('float32')
        # test_set /= 255
        result = rn_model.predict(test_set)
        idx = np.argmax(result)
        output += to_latin(idx)
    return len(output), output


if __name__ == '__main__':
    # images = [r'D:\College_stuff\AN_3_Sem_1\IA\proiect\OCR-manuscripts\Utils_for_DB\BlurredImages\test1-1.jpg']
    # pixels = [np.array(load_image(img) / 255).tolist() for img in images]
    # json_input = json.dumps({'size': len(pixels), 'letters': pixels})
    # with open('rn_input.json', 'w') as f:
    #    f.write(json_input)
    if os.path.exists(MODEL_FILE_NAME):
        rn_model = keras.models.Sequential()
        rn_model.add(InputLayer((784,)))
        rn_model.add(Dropout(0.2))  # inaintea stratului pentru care vrem sa facem drop-out
        rn_model.add(Dense(250, activation='relu'))
        rn_model.add(Dense(113, activation='softmax'))
        rn_model.load_weights(MODEL_FILE_NAME)
    else:
        rn_model = loading_and_training()
        rn_model.save_weights(MODEL_FILE_NAME)
    # while 1:
    #     imagename = input("Enter image name: ")
    #     if imagename == 'exit':
    #         break
    #     # thinning_algorithm.processImage(imagename)
    #     data_to_test = load_image(imagename)
    #     test_set = [data_to_test]
    #     test_set = np.asarray(test_set)
    #     test_set = test_set.astype('float32')
    #     test_set /= 255
    #     result = rn_model.predict(test_set)
    #     idx = np.argmax(result)
    #     print(to_latin(idx))
    # # print("ExpectedOutput: "+to_latin(result))
    my_json = json.load(open("rn_input.json", "rt"))
    for i in range(0, my_json["size"]):
        image = np.array(my_json["letters"][i], dtype=np.float32)
        new_img = [image]
        new_img = np.asarray(new_img)
        result = rn_model.predict(new_img)
        idx = np.argmax(result)
        print(to_latin(idx))
