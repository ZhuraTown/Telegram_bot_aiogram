from flask import Flask, render_template, request, jsonify
from data_base.db_commands import CommandsDB


app = Flask(__name__)


@app.route('/create_form')
def create_form():
    return render_template('create_form.html')


@app.route('/builds', methods=['GET'])
def get_builds():
    builds = {}
    for build in CommandsDB.get_all_names_builds():
        builds[build[0]] = build[1]
    return jsonify(builds)


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


@app.route('/get')
def page_user():
    return render_template('my_get.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)