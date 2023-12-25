const connection = "http://127.0.0.1:8000";

let displayArea = document.getElementById('object-display')



function writeTable(response){
    displayArea.innerHTML = ""
    let keys = Object.keys(response.data[0])
    let tableHTML = `<table><tr>`
    for (let j = 0;j<keys.length;j++) {
        tableHTML += `<th>${keys[j]}</th>`
    }
    tableHTML += `</tr>`
    for (let i = 0;i<response.data.length;i++) {
        let values = Object.values(response.data[i])
        tableHTML += `<tr>`
        for (let j = 0;j<values.length;j++){
            tableHTML += `<td>${values[j]}</td>`
        }
        tableHTML += `</tr>`
    }
    tableHTML += `</table>`
    console.log(tableHTML)
    displayArea.innerHTML = tableHTML
}

function sendSignal(){
    axios.get(connection + '/actor')
        .then((response) => writeTable(response))
        .catch((error) => console.log(error))
};

document.getElementById('test').onclick = sendSignal;
