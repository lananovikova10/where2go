from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")

def display():
    title = 'Куда поехать из России'
    country_name = ['Австралия', 'Австрия', 'Азербайджан', 'Албания', 'Алжир', 'Ангола', 'Андорра', 'Антигуа и Барбуда']
    return render_template('index.html', page_title = title, country_name = country_name)

if __name__=="__main__":
    app.run(debug=True)