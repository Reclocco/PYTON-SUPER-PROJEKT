from flask import Flask, render_template

app = Flask(__name__)


@app.route('/home')
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/generate')
def generate():
    # generate tweets to pass
    tweet = "lorem impsum tralala poka bimboły jak zdać studia tutorial 5 min fast"
    return render_template('generate.html', tweet=tweet)

@app.route('/stats')
def stats():
    # generate twitter statistics data to pass
    data = "UwU t.. twittew-san, hewwo *-*"
    return render_template('stats.html', data=data)


if __name__ == '__main__':
    app.run()
