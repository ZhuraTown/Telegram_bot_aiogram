from datetime import datetime

from flask import Flask, render_template, request, jsonify
from data_base.db_commands import CommandsDB

app = Flask(__name__)


@app.route('/builds', methods=['GET'])
def get_builds():
    builds = {}
    for build in CommandsDB.get_all_names_builds():
        builds[build[0]] = build[1]
    return jsonify(builds)


@app.route('/contactors', methods=['GET'])
def get_contactors():
    contactors = {}
    for company in CommandsDB.get_names_all_users(without_admin=True):
        contactors[company] = company
    return jsonify(contactors)


@app.route('/create_form', methods=['GET', "POST"])
def create_form():
    if request.method == 'POST':
        data = request.form.to_dict(flat=False)
        name_work = data.pop('name_work')[0]
        date = data.pop('date')[0]
        company = data.pop('company')[0]
        contractor = data.pop('contractor')[0]
        form_sheet = {}
        for line in range(0, len(data.get('select'))):
            for key in data.keys():
                if key not in form_sheet:
                    form_sheet[key] = data.get(key)[line]
                else:
                    form_sheet[key] = data.get(key)[line]
            CommandsDB.add_new_string_work(user_name=company, name_work=name_work, contractor=contractor,
                                           name_build=form_sheet.get('select'), level=form_sheet.get('level'),
                                           name_stage=form_sheet.get('stage'),
                                           number_worker=[int(form_sheet['worker_p']), int(form_sheet['worker_f'])],
                                           number_security=[int(form_sheet['sec_p']), int(form_sheet['sec_f'])],
                                           number_duty=[int(form_sheet['duty_p']), int(form_sheet['duty_f'])],
                                           number_itr=[int(form_sheet['itr_p']), int(form_sheet['itr_f'])])
        msg = "Форма успешно отправлена на сервер! Можете закрыть страницу"
        return render_template('finish_create_form.html', company=company, date=date, name_work=name_work, msg=msg)

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
        return data
    elif request.method == "GET":
        return render_template('finish_create_form.html', )


@app.route('/edit_form', methods=['GET', "POST"])
def page_user():
    name_work = request.args.get('work')
    company = request.args.get('company')
    date = datetime.today().strftime('%d.%m.%y')

    if request.method == "POST":
        data = request.form.to_dict(flat=False)

        name_work = data.pop('name_work')[0]
        date = data.pop('date')[0]
        company = data.pop('company')[0]
        contractor = data.pop('contractor')[0]
        form_sheet = {}

        all_ids_edit = data.pop('ids')[0]
        ids_edit = [int(i) for i in data.get('id-str-form')] if data.get('id-str-form') \
            else []
        all_ids_edit = [int(i) for i in all_ids_edit[1:len(all_ids_edit) - 1].replace("'", "").split(',')]

        if data.get('select'):
            for line in range(0, len(data.get('select'))):
                for key in data.keys():
                    if key not in form_sheet:
                        form_sheet[key] = data.get(key)[line] if data.get(key)[line] else 0
                    else:
                        form_sheet[key] = data.get(key)[line] if data.get(key) else 0
                CommandsDB.add_new_string_work(user_name=company, name_work=name_work,
                                               contractor=contractor,
                                               name_build=form_sheet.get('select'),
                                               level=form_sheet.get('level'),
                                               name_stage=form_sheet.get('stage'),
                                               number_worker=[int(form_sheet['worker_p']),
                                                              int(form_sheet['worker_f'])],
                                               number_security=[int(form_sheet['sec_p']),
                                                                int(form_sheet['sec_f'])],
                                               number_duty=[int(form_sheet['duty_p']),
                                                            int(form_sheet['duty_f'])],
                                               number_itr=[int(form_sheet['itr_p']),
                                                           int(form_sheet['itr_f'])])
        form_sheet = {}
        if data.get('select-form'):
            ids = data.get('id-str-form')
            for line in range(0, len(data.get('select-form'))):
                for key in data.keys():
                    if 'form' in key:
                        if key not in form_sheet:
                            form_sheet[key] = data.get(key)[line] if data.get(key)[line] else 0
                        else:
                            form_sheet[key] = data.get(key)[line] if data.get(key) else 0
                CommandsDB.edit_form_string_with_id(
                    id_string=ids[line], name_stage=form_sheet.get('stage-form'),
                    level=form_sheet.get('level-form'),
                    name_build=form_sheet.get('select-form'), contractor=contractor,
                    number_security=[int(form_sheet['sec_p-form']), int(form_sheet['sec_f-form'])],
                    number_duty=[int(form_sheet['duty_p-form']), int(form_sheet['duty_f-form'])],
                    number_worker=[int(form_sheet['worker_p-form']), int(form_sheet['worker_f-form'])],
                    number_itr=[int(form_sheet['itr_p-form']), int(form_sheet['itr_p-form'])],
                )

        if len(ids_edit) != len(all_ids_edit):
            for id_str in all_ids_edit:
                if id_str not in ids_edit:
                    CommandsDB.del_str_form_with_name_work_or_id_form(id_form=id_str)
        msg = 'Форма успешна обновлена! Можете закрыть страницу!'
        return render_template('finish_create_form.html', company=company, date=date, name_work=name_work, msg=msg)

    elif request.method == "GET":
        ids = request.args.get('ids').split(',')
        contractor = request.args.get('contractor')
        forms = {}
        for id_form in ids:
            if CommandsDB.check_that_str_form_with_id_in_db(id_form):
                forms[id_form] = CommandsDB.get_str_form_with_id(id_form)[0]
        return render_template('edit_form.html', forms=forms, name_work=name_work,
                               company=company, date=date, ids=ids, contractor=contractor)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
