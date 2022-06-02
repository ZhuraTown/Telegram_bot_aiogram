
function add_str() {
    const element = document.getElementById("form_timesheet");
    var element_2 = document.createElement('div')
    var id_form = document.getElementById('form')

    element_2.innerHTML = '<div class="form-group">\n' +
        '                    <div class="input-group">\n' +
        '                        <input type="text" class="form-control" placeholder="Этап" name="stage">\n' +
        '                        <input type="text" class="form-control" placeholder="Этаж" name="level">\n' +
        '                        <input type="text" class="form-control" placeholder="Здание" name="build">\n' +
        '                    </div>\n' +
        '                    <div class="input-group">\n' +
        '                        <input type="number" class="form-control" placeholder="Деж.П" name="dej_p">\n' +
        '                        <input type="number" class="form-control" placeholder="Деж.Ф" name="dej_f">\n' +
        '                        <input type="number" class="form-control" placeholder="ИТР.П" name="itr_p">\n' +
        '                        <input type="number" class="form-control" placeholder="ИТР.Ф" name="itr_f">\n' +
        '                    </div>\n' +
        '                            <div class="line-separator"></div>' +
        '                </div>'

    element.append(element_2)
}

let base = document.getElementById('form_timesheet')
let but_del = document.getElementById('clear')

but_del.addEventListener('click', ClearFunction)

function ClearFunction() {
    if (base.lastChild.id === '') {
        base.removeChild(base.lastChild)
    }
}

