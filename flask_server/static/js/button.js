
function add_str() {
    const element = document.getElementById("form");
    var element_2 = document.createElement('div')
    var id_form = document.getElementById('form')

    element_2.innerHTML = '<div class="form-group">\n' +
        '                    <div class="input-group">\n' +
        '                        <input type="text" class="form-control" placeholder="Этап">\n' +
        '                        <input type="text" class="form-control" placeholder="Этаж">\n' +
        '                        <input type="text" class="form-control" placeholder="Здание">\n' +
        '                    </div>\n' +
        '                    <div class="input-group">\n' +
        '                        <input type="number" class="form-control" placeholder="Деж.П">\n' +
        '                        <input type="number" class="form-control" placeholder="Деж.Ф">\n' +
        '                        <input type="number" class="form-control" placeholder="ИТР.П">\n' +
        '                        <input type="number" class="form-control" placeholder="ИТР.Ф">\n' +
        '                    </div>\n' +
        '                            <div class="line-separator"></div>' +
        '                </div>'

    element.append(element_2)
}

let base = document.getElementById('form')
let but_del = document.getElementById('clear')

but_del.addEventListener('click', ClearFunction)

function ClearFunction() {
    if (base.lastChild.id === '') {
        base.removeChild(base.lastChild)
    }
}