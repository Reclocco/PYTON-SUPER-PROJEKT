import difflib
import enchant
import random


def formatPrediction(predictedText):
    # duża litera na początku
    if 96 < ord(predictedText[0]) < 123:
        predictedText = chr(ord(predictedText[0]) - 32) + predictedText[1:]
    # powtarzające się spacje
    predictedText = ' '.join(predictedText.split())
    # wszystkie litery po kropce duże, (pozwala to usunąć duże litery z przetwarzania - to 24 znaki mniej)
    for i in range(len(predictedText)):
        char = ''
        try:
            char = predictedText[i]
        except IndexError:
            pass
        if char == '.':
            try:
                # spacja po kropce ale nie po wielokropku
                if predictedText[i + 1] not in [' ', '.']:
                    predictedText = predictedText[:i + 1] + ' ' + predictedText[i + 1:]
                # duża litera po kropce
                elif predictedText[i + 2] not in ['.', '#', '@']:
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

    # na wypadek gdyby mentions powstało rzeczywiste - dodanie losowej litery
    t = ''
    for char in predictedText:
        t += char
        if char == '@':
            t += chr(random.randint(65, 90))
    predictedText = t

    predictedText = guessWords(predictedText)
    return predictedText


def guessWords(text):
    # istnieją słowa odzielone spacjami, ewentualnie trzeba poprawić jakieś literówki
    # do zastosowania przy bardziej zaawansowanej sieci neuronowej albo po wiekszej ilości treningu
    dictUS = enchant.Dict('en_US')
    dictGB = enchant.Dict('en_GB')
    newText = ''
    for word in text.split():
        if len(word) > 0:
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
    return newText
