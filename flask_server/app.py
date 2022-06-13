from datetime import datetime

from flask import Flask, render_template, request, jsonify
from data_base.db_commands import CommandsDB

app = Flask(__name__)


@app.route('/1', methods=["GET", "POST"])
def example():
    url_args = request.args
    return render_template('example.html',
                           title=url_args.get('title'), name=url_args.get('name'), word=url_args.get('word'))


@app.route('/builds', methods=['GET'])
def get_builds():
    builds = {}
    for build in CommandsDB.get_all_names_builds():
        builds[build[0]] = build[1]
    return jsonify(builds)


@app.route('/create_form', methods=['GET', "POST"])
def create_form():
    if request.method == 'POST':
        data = request.form.to_dict(flat=False)
        name_work = data.pop('name_work')[0]
        date = data.pop('date')[0]
        company = data.pop('company')[0]
        form_sheet = {}
        for line in range(0, len(data.get('select'))):
            for key in data.keys():
                if key not in form_sheet:
                    form_sheet[key] = data.get(key)[line]
                else:
                    form_sheet[key] = data.get(key)[line]
            CommandsDB.add_new_string_work(user_name=company, name_work=name_work,
                                           name_build=form_sheet.get('select'), level=form_sheet.get('level'),
                                           name_stage=form_sheet.get('stage'),
                                           number_worker=[int(form_sheet['worker_p']), int(form_sheet['worker_f'])],
                                           number_security=[int(form_sheet['sec_p']), int(form_sheet['sec_f'])],
                                           number_duty=[int(form_sheet['duty_p']), int(form_sheet['duty_f'])],
                                           number_itr=[int(form_sheet['itr_p']), int(form_sheet['itr_f'])])
        return render_template('finish_create_form.html', company=company, date=date, name_work=name_work)

    elif request.method == "GET":
        name_work = request.args.get('work')
        company = request.args.get('company')
        date = datetime.today().strftime('%d.%m.%y')
        return render_template('create_form.html', company=company,
                               name_work=name_work, date=date)


@app.route('/', methods=['GET', "POST"])
def main_page():
    if request.method == 'POST':
        data = request.form.to_dict(flat=False)
        print(data)
        print(len(data))
        print(type(data))
        return data
    elif request.method == "GET":
        return render_template('finish_create_form.html', )


@app.route('/get')
def page_user():
    return render_template('my_get.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
