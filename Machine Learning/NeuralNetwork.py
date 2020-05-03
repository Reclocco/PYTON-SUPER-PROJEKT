import numpy
import sys
import tensorflow as tf
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint


def check_words(text):
    # TODO zmienić żeby akceptowało tylko [a-zA-Z']
    text = text.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    filtered = filter(lambda token: token not in stopwords.words('english'), tokens)
    return " ".join(filtered)


def generate(training_text, train, weight_file, result_length):
    chars = sorted(list(set(training_text)))
    char_to_num = dict((c, i) for i, c in enumerate(chars))
    num_to_char = dict((i, c) for i, c in enumerate(chars))
    input_len = len(training_text)
    vocab_len = len(chars)
    print("Total number of characters:", input_len)
    print("Total number of different characters:", vocab_len)
    seq_length = 100
    x_data = []
    y_data = []

    for i in range(0, input_len - seq_length, 1):
        input_seq = training_text[i:i + seq_length]
        output = training_text[i + seq_length]
        x_data.append([char_to_num[char] for char in input_seq])
        y_data.append(char_to_num[output])

    n_patterns = len(x_data)
    X = numpy.reshape(x_data, (n_patterns, seq_length, 1))
    # X = X / float(vocab_len)
    y = np_utils.to_categorical(y_data)

    model = Sequential()
    model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(256, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(512, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(128))
    model.add(Dropout(0.2))
    model.add(Dense(y.shape[1], activation='softmax'))

    if train:
        try:
            model.load_weights(weight_file)
        except (OSError, ValueError) as e:
            pass
        model.compile(loss='categorical_crossentropy', optimizer='adam')
        checkpoint = ModelCheckpoint(weight_file, monitor='loss', verbose=1, save_best_only=True, mode='min')
        desired_callbacks = [checkpoint]
        model.fit(X, y, epochs=20, batch_size=128, callbacks=desired_callbacks)
    else:
        try:
            model.load_weights(weight_file)
            model.compile(loss='categorical_crossentropy', optimizer='adam')
        except OSError:
            print("Cannot open weights file")
            return

    start = numpy.random.randint(0, len(x_data) - 1)
    pattern = x_data[start]
    print("Random Starting Pattern:")
    print("\"", ''.join([num_to_char[value] for value in pattern]), "\"")

    generated_text = ''
    for i in range(result_length):
        x = numpy.reshape(pattern, (1, len(pattern), 1))
        # x = x / vocab_len
        prediction = model.predict(x, verbose=0)
        index = numpy.argmax(prediction)
        pattern.append(index)
        pattern = pattern[1:len(pattern)]
        generated_text += num_to_char[index]

    return generated_text


if __name__ == '__main__':
    # TODO get data from twitter
    filename = '.txt'
    file = open(filename).read()
    processed_inputs = check_words(file)
    # False jeżeli chcemy wykorzystać istniejące wagi i wygenerować tekst,
    # True dla trenowania nowych wag
    text = generate(processed_inputs, False, 'weightsFrankenstein.hdf5', 100)
    print(text)

    # IDEAS TO DO TO GET BETTER RESULTS
    # increase the number of training epochs
    # use a deeper neural network (add more layers)
    # use a wider neural network (increase number of neurons / memory units)
    # adjust the batch size
    # one hot-encode the inputs
    # padding the input sequences
