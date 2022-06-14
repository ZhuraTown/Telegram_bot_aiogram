// import { URL_WORK_BUILDS } from '../../../constants'

const URL_WORK_BUILDS = "http://127.0.0.1:5000/builds"


function add_str() {
    const form = document.getElementById("form_timesheet");
    const number_form = document.querySelectorAll('#form_container').length
    const id_form = 'form_' + number_form
    let new_form = document.createElement('div')
    let id_select = 'select_' + number_form
    new_form.id =  id_form
    const form_part_1 =  '<div class="container form-box" id="form_container">\n' +
        '            <div class="form-group">\n' +
        '                <div class="build_stage_level">\n' +
        '                <div class="input_build">\n'

    let form_part_2 = `<select name="select" class="build-select" id="${id_select}" required><option selected value="">Здание</option></select>`
    const form_part_3 = '</div>\n' +
        '                    <div class="input_inline">\n' +
        '                        <div class="left-block" >\n' +
        '                            <input type="text" class="form-control only-block" placeholder="Этаж" name="level" id="level" required>\n' +
        '                        </div>\n' +
        '                        <div class="right-block">\n' +
        '                            <input type="number" class="form-control only-block" placeholder="Этап" name="stage" id="stage" required>\n' +
        '                        </div>\n' +
        '                    </div>\n' +
        '                    </div>\n' +
        '                <div class="workers">\n' +
        '                    <h4>Рабочие</h4>\n' +
        '                    <div class="input_inline">\n' +
        '                        <div class="left-block" >\n' +
        '                            <input type="number" class="form-control only-block" placeholder="Плановый" name="worker_p" id="worker_p" value="0">\n' +
        '                        </div>\n' +
        '                        <div class="right-block">\n' +
        '                            <input type="number" class="form-control only-block" placeholder="Фактический" name="worker_f" id="worker_f" value="0">\n' +
        '                        </div>\n' +
        '                    </div>\n' +
        '                </div>\n' +
        '                <div class="workers">\n' +
        '                    <h4>ИТР</h4>\n' +
        '                    <div class="input_inline">\n' +
        '                        <div class="left-block" >\n' +
        '                            <input type="number" class="form-control only-block" placeholder="Плановый" name="itr_p" id="itr_p" value="0">\n' +
        '                        </div>\n' +
        '                        <div class="right-block">\n' +
        '                            <input type="number" class="form-control only-block" placeholder="Фактический" name="itr_f" id="itr_f" value="0">\n' +
        '                        </div>\n' +
        '                    </div>\n' +
        '                </div>\n' +
        '                <div class="workers">\n' +
        '                    <h4>Охрана</h4>\n' +
        '                    <div class="input_inline">\n' +
        '                        <div class="left-block" >\n' +
        '                            <input type="number" class="form-control only-block" placeholder="Плановый" name="sec_p" id="sec_p" value="0">\n' +
        '                        </div>\n' +
        '                        <div class="right-block">\n' +
        '                            <input type="number" class="form-control only-block" placeholder="Фактический" name="sec_f" id="sec_f" value="0">\n' +
        '                        </div>\n' +
        '                    </div>\n' +
        '                </div>\n' +
        '                <div class="workers">\n' +
        '                    <h4>Дежурный</h4>\n' +
        '                    <div class="input_inline">\n' +
        '                        <div class="left-block" >\n' +
        '                            <input type="number" class="form-control only-block" placeholder="Плановый" name="duty_p" id="duty_p" value="0">\n' +
        '                        </div>\n' +
        '                        <div class="right-block">\n' +
        '                            <input type="number" class="form-control only-block" placeholder="Фактический" name="duty_f" id="duty_f" value="0">\n' +
        '                        </div>\n' +
        '                    </div>\n' +
        '                </div>\n' +
        '                <div class="button-delete">'
    let form_part_4 = `<input type="button" value="Удалить" class="btn delete" id="clear" onclick="del_form('${id_form}');"></div></div></div>`
    new_form.innerHTML = form_part_1 + form_part_2 + form_part_3+ form_part_4
    form.append(new_form)
    getResponseName(id_select)
}

function del_form(id_form) {
    let form_delete = document.getElementById(id_form)
    form_delete.remove()
}

async function getResponse(){
        function addOption(key, value) {
        let newOption = new Option(value, key)
        build.append(newOption)
    }
    // let response = await fetch("http://127.0.0.1:5000/builds",{
    let response = await fetch(URL_WORK_BUILDS,{
        method: "GET"
    } ).then(response => response.json())
    for(let key in response){
        addOption(response[key], response[key])
    }
}

async function getResponseName(id_select){
    function addOption(key, value) {
        let newOption = new Option(value, key)
        let select = document.getElementById(id_select)
        select.append(newOption)
    }
    // let response = await fetch("http://127.0.0.1:5000/builds",{
    let response = await fetch(URL_WORK_BUILDS,{
        method: "GET"
    } ).then(response => response.json())
    for(let key in response){
        addOption(response[key], response[key])
    }
    }

    // const btn = document.querySelector('.btn-add')
    // btn.addEventListener('click', () => {
    //     console.log('hey')
    //     add_str();
    // })

getResponse()




