from flask import Flask, render_template
from config import Config
from forms import LoginForm

app = Flask(__name__)
app.config.from_object(Config)


@app.route("/")

def display():
    title = 'Куда поехать из России'
    country_name = ['Австралия', 'Австрия', 'Азербайджан', 'Албания', 'Алжир', 'Ангола', 'Андорра', 'Антигуа и Барбуда']
    country_code = ['AU', 'AU2', 'AZZ', 'ALD', 'ALZ', 'ANG', 'ANO', 'AAB']
    quant = len(country_name)
    return render_template('index.html', page_title = title, quant = quant, country_name = country_name, country_code = country_code)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)

if __name__=="__main__":
    app.run(debug=True)