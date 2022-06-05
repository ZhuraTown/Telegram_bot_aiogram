

async function getResponse(){
        function addOption(key, value) {
        let newOption = new Option(value, key)
        builds.append(newOption)
    }
    // let response = await fetch("http://127.0.0.1:5000/builds", {
    // let response = await fetch("http://127.0.0.1:5000/builds",{
    let response = await fetch("https://16ce-94-19-112-97.eu.ngrok.io",{
        method: "GET"
    } ).then(response => response.json())
    for(let key in response){
        addOption(key, response[key])
    }

}

getResponse()


