import os
import platform
import sys

import numpy
import datetime
import tensorflow as tf
import keras.backend.tensorflow_backend as tb
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint
from Machine_Learning.textFormating import formatPrediction


# 30 dozwolonych znaków
# (im mniej znaków tym prościej wytrenować)
chars = sorted(
        [chr(i) for i in range(97, 123)] +  # małe litery
        [' ', '#', '@', '.']  # znaki specjalne
    )
# przeliczenie ze znaków na liczby
char_to_num = dict((c, i) for i, c in enumerate(chars))
num_to_char = dict((i, c) for i, c in enumerate(chars))


def getLastWeightFile(topic):
    # pobiera ostatio dodany plik z wagami
    lastDate = datetime.datetime.fromtimestamp(0)
    lastFile = ''
    slash = '/' if platform.system() == 'Linux' else '\\'
    directory = 'Machine_Learning' + slash
    for name in os.listdir(directory):
        if str(topic) + '.hdf5' in name:
            date = datetime.datetime.strptime(name[10:29], '%Y-%m-%d-%H-%M-%S')
            if date > lastDate:
                lastDate = date
                lastFile = name
    return lastFile


def generateModel(text):
    input_len = len(text)
    vocab_len = len(chars)
    print("Total number of characters:", input_len)
    print("Total number of different characters:", vocab_len)
    seq_length = 100
    x_data = []
    y_data = []

    for i in range(0, input_len - seq_length, 1):
        input_seq = text[i:i + seq_length]
        output = text[i + seq_length]
        x_data.append([char_to_num[char] for char in input_seq])
        y_data.append(char_to_num[output])

    n_patterns = len(x_data)
    X = numpy.reshape(x_data, (n_patterns, seq_length, 1))
    X = X / float(vocab_len)
    Y = np_utils.to_categorical(y_data)

    tb._SYMBOLIC_SCOPE.value = True
    model = Sequential()
    model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(512, return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(512))
    model.add(Dropout(0.1))
    model.add(Dense(Y.shape[1], activation='softmax'))

    return model, X, Y, x_data


def train(text, epoch_n, batch_s, topic):
    model, X, Y, _ = generateModel(text)
    try:
        last_weight_file = os.path.dirname(os.getcwd()) + '/Machine_Learning/' + getLastWeightFile(topic)
        model.load_weights(last_weight_file)
        print(f'model loaded {last_weight_file}')
    except OSError:
        print('no model loaded')
    except ValueError:
        print('no model for specified network size')
    new_weight_file = 'weights - ' + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ' - ' + topic + '.hdf5'
    print(new_weight_file)
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    checkpoint = ModelCheckpoint(new_weight_file, monitor='loss', verbose=1, save_best_only=True, mode='min')
    desired_callbacks = [checkpoint]
    model.fit(X, Y, epochs=epoch_n, batch_size=batch_s, callbacks=desired_callbacks)


def createTweet(text, result_length, topic):
    model, _, _, x_data = generateModel(text)
    try:
        slash = '/' if platform.system() == 'Linux' else '\\'
        last_weight_file = 'Machine_Learning' + slash + getLastWeightFile(topic)
        model.load_weights(last_weight_file)
        print(f'model loaded {last_weight_file}')
        model.compile(loss='categorical_crossentropy', optimizer='adam')
    except (OSError, ValueError):
        print(sys.exc_info()[0])
        print("Cannot open weights file")
        return ''

    start = numpy.random.randint(0, len(x_data) - 1)
    pattern = x_data[start]
    vocab_len = len(chars)
    generated_text = ''
    for i in range(result_length):
        x = numpy.reshape(pattern, (1, len(pattern), 1))
        x = x / vocab_len
        prediction = model.predict(x, verbose=0)

        # chooces one with max probability
        index = numpy.argmax(prediction)

        pattern.append(index)
        pattern = pattern[1:len(pattern)]
        generated_text += num_to_char[index]

    return formatPrediction(generated_text)


'''
    zastosowane modele:
    (L-LSTM, D-Dropout)
    1. L256 + D.3 + L512 + D.3 + L1024 + D.2 + L512 + D.2 + L256 + D.1 + Dense
    2. L256 + D.3 + L512 + D.3 + L512 + D.2 + L256 + D.1 + Dense
    3. L256 + D.3 + L512 + D.3 + L256 + D.1 + Dense
    4. L256 + D.3 + L512 + D.3 + L512 + D.1 + Dense

    rozmiar danych ~ 100 000 znaków

    STATS:
    dozwolone znaki | model | epoch | batch | loss  | średni czas na epoch
    40              | 1     | 7     | 256   | 3.06  | 1h 45min
    30              | 1     | 1     | 256   | 3.05  | 1h 30min
    30              | 2     | 1     | 256   | 3.02  | 50min
    30              | 3     | 1     | 256   | 3.01  | 27min
    30              | 4     | 17    | 256   | 0.33  | 35min

    UWAGI:
    * zmiana z 40 na 30 dozwolonych znaków (bez cyfr) znacznie przyspieszyła naukę - te
        same efekty po 1 epochu, jak po 7 wcześniej
    * zmiana rozmiiaru sieci z łącznej ilości komórek 2560 do 1536 znacznie zmiejszyła
        czas pracy na jeden epoch (uwaga: za duża ilość komórek też może być zła dla
        wygajności sieci)
    * optymalna ilość neuronów na poziomie 1270 +- 128 (dla 30 znaków) czyli model 4
    * batch (typowo 64-512, musi być podzielne na 8)
        medium.com/@canerkilinc/selecting-optimal-lstm-batch-size-63066d88b96b
        "it has been observed that when using a larger batch there is a significant
        degradation in quiality (measured as ability to generalize)"
        stats.stackexchange.com/questions/164876/tradeoff-batch-size-vs-number-of-iterations-to-train-a-neural-network
        (na podstawwie prób optymalne wychodzi 256)
'''