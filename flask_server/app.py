from flask import Flask, render_template

app = Flask(__name__)


@app.route('/create_form')
def create_form():
    return render_template('create_form.html')



@app.route('/')
def main_page():
    return render_template('main.html')

