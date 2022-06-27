from datetime import datetime

from flask import Flask, render_template, request, jsonify
from data_base.db_commands import CommandsDB

app = Flask(__name__)


@app.route('/builds', methods=['GET'])
def get_builds():
    """ Запрос к БД для получения Зданий привязанных к Ген Подрядчику """
    builds = {}
    cont_id = request.args.get('cont')
    for build in CommandsDB.get_all_builds_with_id_gp(cont_id):
        builds[build[1]] = build[1]
    return jsonify(builds)


@app.route('/create_form', methods=['GET', "POST"])
def create_form():
    if request.method == 'POST':
        data = request.form.to_dict(flat=False)
        name_work = data.pop('name_work')[0]
        date = data.pop('date')[0]
        company = data.pop('company')[0]
        contractor = data.pop('contractor')[0]
        user_id = data.pop('comp_id')[0]
        gp_id = data.pop('cont_id')[0]
        form_sheet = {}
        for line in range(0, len(data.get('select'))):
            for key in data.keys():
                if key not in form_sheet:
                    form_sheet[key] = data.get(key)[line]
                else:
                    form_sheet[key] = data.get(key)[line]
            if gp_id == user_id:
                CommandsDB.add_new_string_work(user_name=company, name_work=name_work, contractor=contractor,
                                               is_gp=True,
                                               name_build=form_sheet.get('select'), level=form_sheet.get('level'),
                                               name_stage=int(form_sheet.get('stage')),
                                               number_worker=[int(form_sheet['worker_p']), int(form_sheet['worker_f'])],
                                               number_security=[int(form_sheet['sec_p']), int(form_sheet['sec_f'])],
                                               number_duty=[int(form_sheet['duty_p']), int(form_sheet['duty_f'])],
                                               number_itr=[int(form_sheet['itr_p']), int(form_sheet['itr_f'])],
                                               id_gp=int(gp_id))
            else:
                CommandsDB.add_new_string_work(user_name=company, name_work=name_work, contractor=contractor,
                                               is_gp=False,
                                               name_build=form_sheet.get('select'), level=form_sheet.get('level'),
                                               name_stage=int(form_sheet.get('stage')),
                                               number_worker=[int(form_sheet['worker_p']), int(form_sheet['worker_f'])],
                                               number_itr=[int(form_sheet['itr_p']), int(form_sheet['itr_f'])],
                                               number_duty=[0, 0],
                                               number_security=[0, 0],
                                               id_gp=int(gp_id))

        msg = "Форма успешно отправлена на сервер! Можете закрыть страницу"
        return render_template('finish_create_form.html', company=company, date=date, name_work=name_work, msg=msg)

    elif request.method == "GET":
        cont_id = request.args.get('cont_id')
        name_work = request.args.get('work')
        company = request.args.get('company')
        company_id = request.args.get('comp_id')
        date = datetime.today().strftime('%d.%m.%y')
        contractor = request.args.get('cont')
        is_gp = bool(int(request.args.get('is_gp')))
        if is_gp:
            return render_template('create_form_GP.html', company=company, comp_id=company_id,
                                   name_work=name_work, date=date, cont_id=cont_id, contractor=contractor)
        else:
            return render_template('create_form_user.html', company=company, comp_id=company_id,
                                   name_work=name_work, date=date, cont_id=cont_id, contractor=contractor)


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

    if request.method == "POST":
        data = request.form.to_dict(flat=False)

        name_work = data.pop('name_work')[0]
        date = data.pop('date')[0]
        company = data.pop('company')[0]
        contractor = data.pop('contractor')[0]
        user_id = data.pop('comp_id')[0]
        gp_id = data.pop('cont_id')[0]
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
                if gp_id == user_id:
                    CommandsDB.add_new_string_work(user_name=company, name_work=name_work, contractor=contractor,
                                                   is_gp=True,
                                                   name_build=form_sheet.get('select'), level=form_sheet.get('level'),
                                                   name_stage=int(form_sheet.get('stage')),
                                                   number_worker=[int(form_sheet['worker_p']),
                                                                  int(form_sheet['worker_f'])],
                                                   number_security=[int(form_sheet['sec_p']), int(form_sheet['sec_f'])],
                                                   number_duty=[int(form_sheet['duty_p']), int(form_sheet['duty_f'])],
                                                   number_itr=[int(form_sheet['itr_p']), int(form_sheet['itr_f'])],
                                                   id_gp=int(gp_id))
                else:
                    CommandsDB.add_new_string_work(user_name=company, name_work=name_work, contractor=contractor,
                                                   is_gp=False,
                                                   name_build=form_sheet.get('select'), level=form_sheet.get('level'),
                                                   name_stage=int(form_sheet.get('stage')),
                                                   number_worker=[int(form_sheet['worker_p']),
                                                                  int(form_sheet['worker_f'])],
                                                   number_itr=[int(form_sheet['itr_p']), int(form_sheet['itr_f'])],
                                                   number_duty=[0, 0],
                                                   number_security=[0, 0],
                                                   id_gp=int(gp_id))
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
                if gp_id == user_id:
                    CommandsDB.edit_form_string_with_id(
                        id_string=ids[line], name_stage=form_sheet.get('stage-form'),
                        level=form_sheet.get('level-form'),
                        name_build=form_sheet.get('select-form'), contractor=contractor,
                        number_security=[int(form_sheet['sec_p-form']), int(form_sheet['sec_f-form'])],
                        number_duty=[int(form_sheet['duty_p-form']), int(form_sheet['duty_f-form'])],
                        number_worker=[int(form_sheet['worker_p-form']), int(form_sheet['worker_f-form'])],
                        number_itr=[int(form_sheet['itr_p-form']), int(form_sheet['itr_p-form'])],
                    )
                else:
                    CommandsDB.edit_form_string_with_id(
                        id_string=ids[line], name_stage=form_sheet.get('stage-form'),
                        level=form_sheet.get('level-form'),
                        name_build=form_sheet.get('select-form'), contractor=contractor,
                        number_security=[0, 0],
                        number_duty=[0, 0],
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
        company_id = request.args.get('comp_id')
        cont_id = request.args.get('cont_id')
        date = datetime.today().strftime('%d.%m.%y')
        contractor = request.args.get('cont')
        is_gp = bool(int(request.args.get('is_gp')))

        forms = {}
        for id_form in ids:
            if CommandsDB.check_that_str_form_with_id_in_db(id_form):
                forms[id_form] = CommandsDB.get_str_form_with_id(id_form)[0]
        if is_gp:
            return render_template('edit_form_GP.html', forms=forms, name_work=name_work,
                                   company=company, date=date, ids=ids, contractor=contractor,
                                   comp_id=company_id, cont_id=cont_id)
        else:
            return render_template('edit_form_USER.html', forms=forms, name_work=name_work,
                                   company=company, date=date, ids=ids, contractor=contractor,
                                   comp_id=company_id, cont_id=cont_id)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
