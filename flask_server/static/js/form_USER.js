
const URL_WORK = "http://127.0.0.1:5000/"


function add_str() {
    const form = document.getElementById("form_timesheet");
    let number_form = document.querySelectorAll('#form_container').length
    let id_form = 'form_' + number_form
    while(document.getElementById(id_form) != null){
        number_form ++
        id_form = 'form_' + number_form
    }
    let new_form = document.createElement('div')
    let id_select = 'select_' + number_form
    new_form.id =  id_form
    const form_part_1 =  '<div class="container form-box" id="form_container">\n' +
        '            <div class="form-group">\n' +
        '                <div class="build_stage_level">\n' +
        '                <div class="input_build">\n'

    let form_part_2 = `<select name="select" class="build-select" id="${id_select}" required><option value="" disabled selected>Здание</option></select>`
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
        '                </div>\n' +
        '                <div class="button-delete">'
    let form_part_4 = `<input type="button" value="Удалить" class="btn delete" id="btn-clear" onclick="del_form('${id_form}');"></div></div></div>`
    new_form.innerHTML = form_part_1 + form_part_2 + form_part_3+ form_part_4
    form.append(new_form)
    getBuildsWithIdForm(id_select)
}

function del_form(id_form) {
    let form_delete = document.getElementById(id_form)
    form_delete.remove()
}

async function getBuildForStateForm(){
        function addOption(key, value, element) {
        let newOption = new Option(value, key)
        element.append(newOption)
    }
    let only_build = document.getElementById('build')
    let id_contractor = document.getElementById('cont_id').value
    if (only_build != null){
    let response = await fetch(URL_WORK + "builds" + `?&cont=${id_contractor}`,{
        method: "GET"
    } ).then(response => response.json())
    for(let key in response){
        addOption(response[key], response[key], only_build)
    }}
}

async function getBuildsWithIdForm(id_select){
    function addOption(key, value) {
        let newOption = new Option(value, key)
        let select = document.getElementById(id_select)
        select.append(newOption)
    }
    let id_contractor = document.getElementById('cont_id').value
    let response = await fetch(URL_WORK + "builds" + `?&cont=${id_contractor}`,{
        method: "GET"
    } ).then(response => response.json())
    for(let key in response){
        addOption(response[key], response[key])
    }
    }


async function getBuilds(){
        function addOption(key, value, element) {
        let newOption = new Option(value, key)
        element.append(newOption)
        }
    //    Запрашиваю имена зданий
    let id_contractor = document.getElementById('cont_id').value
    let response = await fetch(URL_WORK + "builds" + `?&cont=${id_contractor}`,{
        method: "GET"
    } ).then(response => response.json())
    //  Собираю список всех доступных полей select, куда добавить здания
    let builds = document.querySelectorAll("#build-form")
    builds.forEach(function(item, i, arr) {
        for(let key in response){
            if (item.children[0].value !== response[key]) {
                addOption(response[key], response[key], item)
            }}})
}


let btn_add = document.getElementById('btn-add')

btn_add.addEventListener('click', add_str)


getBuildForStateForm()
getBuilds()




