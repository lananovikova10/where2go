from flask import Flask, render_template
from webapp.config import Config
from webapp.forms import LoginForm

app = Flask(__name__)
app.config.from_object(Config)

@app.route("/")
def display():
    title = 'Куда поехать из России'
    return render_template('index.html', page_title = title)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)

if __name__=="__main__":
    app.run(debug=True)