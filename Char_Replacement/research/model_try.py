import pickle
import gzip
import keras
from keras.models import Sequential
from keras.layers import InputLayer, Dense, Dropout

import matplotlib.pyplot as plt
from keras.utils import plot_model


def load_dataset():
    with gzip.open('mnist.pkl.gz', 'rb') as f:
        return pickle.load(f, encoding='latin1')


input_set = [["sigmoid", "", "softmax"], ["sigmoid", "softmax", "softmax"],
             ["sigmoid", "", "tanh"], ["sigmoid", "tanh", "tanh"],
             ["relu", "", "softmax"], ["relu", "", "softmax"],
             ["sigmoid", "", "elu"], ["sigmoid", "softmax", "elu"],
             ["sigmoid", "", "selu"], ["sigmoid", "softmax", "selu"],
             ["sigmoid", "", "softplus"], ["sigmoid", "softmax", "softplus"],
             ["sigmoid", "", "softsign"], ["sigmoid", "softmax", "softsign"],
             ["sigmoid", "", "relu"], ["sigmoid", "softmax", "relu"],
             ["sigmoid", "", "softsign"], ["sigmoid", "softmax", "softsign"],
             ]

#for i in range(17):
#    with open(f"out{i}.txt", 'r') as f:
#        with open(f"out{i}{i}.txt", 'w') as g:
#            lines = f.read()
#            g.write(','.join(input_set[i]) + "\n")
#            g.write(lines)
index = 17
data_input = input_set[index]
train_set, valid_set, test_set = load_dataset()
x_train = train_set[0]
y_train = keras.utils.to_categorical(train_set[1], num_classes=10)
x_valid = valid_set[0]
y_valid = keras.utils.to_categorical(valid_set[1], num_classes=10)
x_test = test_set[0]
y_test = keras.utils.to_categorical(test_set[1], num_classes=10)

model = keras.models.Sequential()
model.add(InputLayer((784,)))
model.add(Dropout(0.25))
model.add(Dense(100, activation=data_input[0]))
if data_input[1] is not "":
     model.add(Dense(100, activation=data_input[1]))
model.add(Dense(10, activation=data_input[2]))
model.compile(optimizer=keras.optimizers.SGD(lr=0.1),
              loss="categorical_crossentropy", metrics=["accuracy"])
history = model.fit(x_train, y_train, epochs=5, batch_size=32, verbose=1)
#print(history.history.items())
plt.plot(history.history['loss'])
plt.plot(history.history['acc'])
plt.title('Model accuracy')
plt.ylabel('Loss')
plt.xlabel('Acc')
plt.legend(['Loss', 'Acc'], loc='upper left')
plt.savefig(f'train{index}.png')
plot_model(model, show_shapes=True, show_layer_names=True, to_file=f'model{index}.png')
loss, acc = model.evaluate(x_test, y_test)
with open(f"out{index}.txt", "w") as f:
    f.write("Loss: {}; Acc: {}".format(loss, acc))
