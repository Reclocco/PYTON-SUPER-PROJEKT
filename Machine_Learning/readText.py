import os
import enchant
# from Machine_Learning.NeuralNetwork import train, createTweet


# 40 dozwolonych znaków (ewentualnie można pozbyć się cyfr)
# im mniej znaków tym prościej wytrenować
chars = sorted(
    # [str(i) for i in range(10)] +  # cyfry
    [chr(i) for i in range(97, 123)] +  # małe litery
    [' ', '#', '@', '.']  # znaki specjalne
)
# słowniki
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


if __name__ == '__main__':
    # musi być zaimportowane tu, aby uniknąć 'circular imports'
    from Machine_Learning.NeuralNetwork import train, createTweet

    filename = os.path.dirname(os.getcwd()) + '/Data_Collection/trump - hasztag - 2020-05-05.txt'
    file = open(filename).read()
    englishText = areWordsEnglish(file)
    # train(englishText, 16, 256)
    text = createTweet(englishText, 100)
    print("\"" + text + "\"")
