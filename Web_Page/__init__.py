from flask import Flask, render_template

app = Flask(__name__)


@app.route('/home')
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/generate')
def generate():
    # generate tweets to pass them to website
    tweet = "random text"
    return render_template('generate.html', tweet=tweet)


if __name__ == '__main__':
    app.run()
