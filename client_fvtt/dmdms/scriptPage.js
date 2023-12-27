const connection = "http://127.0.0.1:8000";

let displayArea = document.getElementById('object-display')
let singleDisplay = document.getElementById('single-display')

function writeTable(response, endpoint){
    displayArea.innerHTML = ""
    let keys = Object.keys(response.data[0])
    let tableHTML = `<table><tr>`
    for (let j = 0;j<keys.length;j++) {
        tableHTML += `<th>${keys[j]}</th>`
    }
    tableHTML += `</tr>`
    // displayArea.innerHTML += tableHTML
    for (let i = 0;i<response.data.length;i++) {
        let values = Object.values(response.data[i])
        tableHTML += `<tr>`
        tableHTML += `<td><button id='${values[0]}-${values[1]}'>${values[0]}</button></td>`
        for (let j = 1;j<values.length;j++){
            tableHTML += `<td>${values[j]}</td>`
        }
        tableHTML += `</tr>`
        displayArea.innerHTML += tableHTML
        // console.log(`${values[0]}-${values[1]}`)
        // document.getElementById(`${values[0]}-${values[1]}`).onclick = () => console.log(`${endpoint}/?id=${values[0]}`)
    }
    tableHTML += `</table>`
    displayArea.innerHTML = tableHTML
    for (let i = 0;i<response.data.length;i++){
        let values = Object.values(response.data[i])
        document.getElementById(`${values[0]}-${values[1]}`).onclick = () => sendOneSignal(`${endpoint}/?id=${values[0]}`)
    }
}

function writeOne(data) {
    singleDisplay.innerHTML = '';
    let { overview, traits, related } = data
    // console.log(overview)
    singleDisplay.innerHTML += '<h2>Overview</h2><ul>'
    for (const property in overview) {
        singleDisplay.innerHTML += `<li>${property}: ${overview[property]}</li>`
    }
    singleDisplay.innerHTML += '</ul>'
    singleDisplay.innerHTML += '<h2>Traits</h2>'
    for (const property in traits) {
        singleDisplay.innerHTML += `<h3>${property}</h3><ul>`
        let currentTrait = traits[property] // this is where we'll ask for a name to make a card?
        for (let i = 0;i<currentTrait.length;i++) {
            let currentItem = currentTrait[i]
            for (const j in currentItem) {
                singleDisplay.innerHTML += `<li>${j}: ${currentItem[j]}</li>`
            }
        }
        singleDisplay.innerHTML += `</ul>`
    }
    singleDisplay.innerHTML += '<h2>Related</h2><ul>'
    // console.log(related)
    for (const property in related) {
        singleDisplay.innerHTML += `<h3>${property}</h3><ul>`
        let currentProperty = related[property] //this is where we'll ask for an event name to make the card
        for (const i in currentProperty) {
            let currentItem = currentProperty[i]
            for (const j in currentItem) {
                singleDisplay.innerHTML += `<li>${j}: ${currentItem[j]}</li>`
            }
        }
        singleDisplay.innerHTML += `</ul>`
    }
    // console.log(relatedValues)
}

function sendOneSignal(endpoint) {
    axios.get(connection + endpoint)
        .then((response) => writeOne(response.data))
        .catch((error) => console.log(error))
}

function sendSignal(endpoint) {
    axios.get(connection + endpoint)
        .then((response) => writeTable(response, endpoint))
        .catch((error) => console.log(error))
}

document.getElementById('dmdmds-actor-btn').onclick = () => sendSignal('/actor');
document.getElementById('dmdmds-faction-btn').onclick = () => sendSignal('/faction');
document.getElementById('dmdmds-location-btn').onclick = () => sendSignal('/location');
document.getElementById('dmdmds-historical-fragments-btn').onclick = () => sendSignal('/historical-fragments');
document.getElementById('dmdmds-object-btn').onclick = () => sendSignal('/object');
document.getElementById('dmdmds-world-data-btn').onclick = () => sendSignal('/world-data');
