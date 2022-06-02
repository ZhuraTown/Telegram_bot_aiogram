from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/create_form')
def create_form():
    return render_template('create_form.html')



@app.route('/', methods=['GET', "POST"])
def main_page():
    if request.method == 'POST':
        data = request.form
        print(data)
        print(len(data))
        print(type(data))
        return data
    elif request.method == "GET":
        # return render_template('main.html')
        return render_template('create_form_sheet.html')


@app.route('/user/<string:username>')
def page_user(username):
    return render_template('index.html', username=username)


if __name__ == '__main__':
    app.run(debug=True, port=5000)