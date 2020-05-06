import os
import numpy
import enchant
import difflib
import datetime
import random
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint


# 40 dozwolonych znaków (ewentualnie można pozbyć się cyfr) - im mniej znaków tym prościej wytrenować
chars = sorted(
    # [str(i) for i in range(10)] +  # cyfry
    [chr(i) for i in range(97, 123)] +  # małe litery
    [' ', '#', '@', '.']  # znaki specjalne
)
char_to_num = dict((c, i) for i, c in enumerate(chars))
num_to_char = dict((i, c) for i, c in enumerate(chars))
dictUS = enchant.Dict('en_US')
dictGB = enchant.Dict('en_GB')


def areWordsEnglish(text):
    # średnio 75% treści tweetów jest jakimis realnymi słowami
    text = text.lower()
    # change interpunction to .
    d = {'!': '.', '?': '.'}
    text = ''.join(map(lambda c: d[c] if c in d else c, text))
    # allow only specified chars
    text = ''.join((c for c in text if c in chars))
    formattedText = ''
    for word in text.split(' '):
        try:
            # correct english words
            if dictUS.check(word) or dictGB.check(word):
                formattedText += word + ' '
            # hashtags and mentions
            elif word[0] in ['#', '@']:
                formattedText += word + ' '
            else:
                # znaki interpunkcyjne
                if '.' in word and word.index('.') != len(word) - 1:
                    i = word.index('.')
                    formattedText += word[:i + 1] + ' ' + word[i + 1:] + ' '
                # cyfry
                if float(word) == word:
                    formattedText += word + ' '
        except ValueError:
            pass
    return formattedText


def getLastWeightFile():
    # pobiera ostatio dodany plik z wagami
    lastDate = datetime.datetime.fromtimestamp(0)
    lastFile = ''
    for name in os.listdir(os.getcwd()):
        if '.hdf5' in name:
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

    model = Sequential()
    model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(512, return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(512))
    model.add(Dropout(0.1))
    model.add(Dense(Y.shape[1], activation='softmax'))

    return model, X, Y, x_data


def train(text, epoch_n, batch_s):
    model, X, Y, _ = generateModel(text)
    try:
        last_weight_file = getLastWeightFile()
        model.load_weights(last_weight_file)
        print(f'model loaded {last_weight_file}')
    except OSError:
        print('no model loaded')
    except ValueError:
        print('no model for specified network size')
    new_weight_file = 'weights - ' + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.hdf5'
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    checkpoint = ModelCheckpoint(new_weight_file, monitor='loss', verbose=1, save_best_only=True, mode='min')
    desired_callbacks = [checkpoint]
    model.fit(X, Y, epochs=epoch_n, batch_size=batch_s, callbacks=desired_callbacks)


def createTweet(text, result_length):
    model, _, _, x_data = generateModel(text)
    try:
        last_weight_file = getLastWeightFile()
        model.load_weights(last_weight_file)
        print(f'model loaded {last_weight_file}')
        model.compile(loss='categorical_crossentropy', optimizer='adam')
    except (OSError, ValueError):
        print("Cannot open weights file")
        return ''

    start = numpy.random.randint(0, len(x_data) - 1)
    pattern = x_data[start]
    print("Random Starting Pattern:")
    print("\"", ''.join([num_to_char[value] for value in pattern]), "\"")
    vocab_len = len(chars)
    generated_text = ''
    for i in range(result_length):
        x = numpy.reshape(pattern, (1, len(pattern), 1))
        x = x / vocab_len
        prediction = model.predict(x, verbose=0)

        # chooces one with max probability
        index = numpy.argmax(prediction)

        # chooses one of best 3 at random
        indexes = numpy.flip(numpy.argpartition(prediction[0], -3)[-3:])
        index = random.choice(indexes)

        # choose one of best 3 with weighted probability
        indexes = numpy.flip(numpy.argpartition(prediction[0], -3)[-3:])
        weights = list(prediction[0][indexes])
        normalizedWeights = weights / sum(weights)
        index = numpy.random.choice(indexes, 1, True, normalizedWeights)[0]

        # choose one of best 3 with squared weighted probability
        indexes = numpy.flip(numpy.argpartition(prediction[0], -3)[-3:])
        weights = list(map(lambda x: x**2, list(prediction[0][indexes])))
        normalizedWeights = weights / sum(weights)
        index = numpy.random.choice(indexes, 1, True, normalizedWeights)[0]

        pattern.append(index)
        pattern = pattern[1:len(pattern)]
        generated_text += num_to_char[index]

    return formatPrediction(generated_text)


def formatPrediction(predictedText):
    print(f'created by NN: \t\t\t"{predictedText}"')
    # duża litera na początku
    if 96 < ord(predictedText[0]) < 123:
        predictedText = chr(ord(predictedText[0]) - 32) + predictedText[1:]
    # powtarzające się spacje
    predictedText = ' '.join(predictedText.split())
    # wszystkie litery po kropce duże, (pozwala to usunąć duże litery z przetwarzania - to 24 znaki mniej)
    for i in range(len(predictedText)):
        char = predictedText[i]
        if char == '.':
            try:
                # spacja po kropce ale nie po wielokropku
                if predictedText[i + 1] not in [' ', '.']:
                    predictedText = predictedText[:i + 1] + ' ' + predictedText[i + 1:]
                # duża litera po kropce
                elif predictedText[i + 2] != '.':
                    print(ord(predictedText[i + 2]))
                    predictedText = predictedText[:i + 2] + chr(
                        max([ord(predictedText[i + 2]) - 32, 0])) + predictedText[i + 3:]
            except IndexError:
                pass
        # po tych znakach nie powinno być spacji
        elif char in ['#', '@']:
            try:
                if predictedText[i+1] == ' ':
                    predictedText = predictedText[:i+1] + predictedText[i+2:]
            except IndexError:
                predictedText = predictedText[:i+1]
    print(f'po zmianie wielkosci: \t"{predictedText}"')

    predictedText = guessWords(predictedText)
    print(f'po zgadywaniu: \t\t\t"{predictedText}"')
    return predictedText


def guessWords(text):
    # wersja jeden - dużo spacji, trzeba jakoś łączyć i zgadywać słowa
    c = 0
    word = ''
    words = []
    collections = [0]
    while c < len(text):
        while c < len(text) and ((max(collections) < 0.85 and len(word) < 10) or len(word) < 2):
            word += text[c]
            c += 1
            suggestions = set(dictUS.suggest(word) + dictGB.suggest(word))
            collections = [difflib.SequenceMatcher(None, word, s).ratio() for s in suggestions]
        words.append(word)
        word = ''
        collections = [0]
    newText = ''
    for word in words:
        if dictUS.check(word) or dictGB.check(word):
            newText += word + ' '
        else:
            bestMatch = word
            highestValue = 0
            suggestions = set(dictUS.suggest(word) + dictGB.suggest(word))
            for s in suggestions:
                val = difflib.SequenceMatcher(None, word, s).ratio()
                if val > highestValue:
                    highestValue = val
                    bestMatch = s
            newText += bestMatch + ' '

    # wersja dwa - istnieją słowa odzielone spacjami, ewentualnie trzeba poprawić jakieś literówki
    # do zastosowania przy bardziej zaawansowanej sieci neuronowej albo po wiekszej ilości treningu
    # newText = ''
    # for word in text.split():
    #     if dictUS.check(word) or dictGB.check(word):
    #         newText += word + ' '
    #     else:
    #         bestMatch = word
    #         highestValue = 0
    #         suggestions = set(dictUS.suggest(word) + dictGB.suggest(word))
    #         for s in suggestions:
    #             val = difflib.SequenceMatcher(None, word, s).ratio()
    #             if val > highestValue:
    #                 highestValue = val
    #                 bestMatch = s
    #         newText += bestMatch + ' '

    return newText


def testPredictingMethod(text):
    # sprawdza która metoda wybierania argumentu z przewidywań (funkcja cerateTweet) jest najlepsza
    model, _, _, x_data = generateModel(text)
    try:
        last_weight_file = getLastWeightFile()
        model.load_weights(last_weight_file)
        print(f'model loaded {last_weight_file}')
        model.compile(loss='categorical_crossentropy', optimizer='adam')
    except (OSError, ValueError):
        print("Cannot open weights file")
        return ''

    start = numpy.random.randint(0, len(x_data) - 1)
    pattern = x_data[start]
    print("Random Starting Pattern:")
    print("\"", ''.join([num_to_char[value] for value in pattern]), "\"")
    vocab_len = len(chars)

    # Method 1 - chooces one with max probability
    pattern = x_data[start]
    generated_text = ''
    for i in range(100):
        x = numpy.reshape(pattern, (1, len(pattern), 1))
        x = x / vocab_len
        prediction = model.predict(x, verbose=0)
        index = numpy.argmax(prediction)
        pattern.append(index)
        pattern = pattern[1:len(pattern)]
        generated_text += num_to_char[index]
    print(f'Method #1: "{generated_text}"')

    # Method 2 - chooses one of best 3 at random
    pattern = x_data[start]
    generated_text = ''
    for i in range(100):
        x = numpy.reshape(pattern, (1, len(pattern), 1))
        x = x / vocab_len
        prediction = model.predict(x, verbose=0)
        indexes = numpy.flip(numpy.argpartition(prediction[0], -3)[-3:])
        index = random.choice(indexes)
        pattern.append(index)
        pattern = pattern[1:len(pattern)]
        generated_text += num_to_char[index]
    print(f'Method #2: "{generated_text}"')

    # Method 3 - choose one of best 3 with weighted probability
    pattern = x_data[start]
    generated_text = ''
    for i in range(100):
        x = numpy.reshape(pattern, (1, len(pattern), 1))
        x = x / vocab_len
        prediction = model.predict(x, verbose=0)
        indexes = numpy.flip(numpy.argpartition(prediction[0], -3)[-3:])
        weights = list(prediction[0][indexes])
        normalizedWeights = weights / sum(weights)
        index = numpy.random.choice(indexes, 1, True, normalizedWeights)[0]
        pattern.append(index)
        pattern = pattern[1:len(pattern)]
        generated_text += num_to_char[index]
    print(f'Method #3: "{generated_text}"')

    # Method 4 - choose one of best 3 with squared weighted probability
    pattern = x_data[start]
    generated_text = ''
    for i in range(100):
        x = numpy.reshape(pattern, (1, len(pattern), 1))
        x = x / vocab_len
        prediction = model.predict(x, verbose=0)
        indexes = numpy.flip(numpy.argpartition(prediction[0], -3)[-3:])
        weights = list(map(lambda x: x ** 2, list(prediction[0][indexes])))
        normalizedWeights = weights / sum(weights)
        index = numpy.random.choice(indexes, 1, True, normalizedWeights)[0]
        pattern.append(index)
        pattern = pattern[1:len(pattern)]
        generated_text += num_to_char[index]
    print(f'Method #4: "{generated_text}"')


if __name__ == '__main__':
    filename = os.path.dirname(os.getcwd()) + '/Data_Collection/trump - hasztag - 2020-05-05.txt'
    file = open(filename).read()
    englishText = areWordsEnglish(file)
    # train(englishText, 16, 256)
    # text = createTweet(englishText, 100)
    # print("\"" + text + "\"")
    testPredictingMethod(englishText)

    # IDEAS TO DO TO GET BETTER RESULTS
    # increase the number of training epochs
    # use a deeper neural network (add more layers)
    # use a wider neural network (increase number of neurons / memory units)
    # adjust the batch size
    # one hot-encode the inputs
    # padding the input sequences

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
    30              | 4     | 1     | 256   | 2.81  | 35min
    
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
        (prawdopodobnie optymalnie będzie któreś z 128, 256, 384
    '''