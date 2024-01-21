// const { default: axios } = require("axios")

let actorButton = document.getElementById('dmdms-actor-btn')
let factionButton = document.getElementById('dmdms-faction-btn')
let locationButton = document.getElementById('dmdms-location-btn')
let historicalFragmentsButton = document.getElementById('dmdms-historical-fragments-btn')
let objectButton = document.getElementById('dmdms-object-btn')
let worldDataButton = document.getElementById('dmdms-world-data-btn')
actorButton.onclick = ev => {sendSignal('/actor')};
factionButton.onclick = ev => {sendSignal('/faction')};
locationButton.onclick = ev => {sendSignal('/location')};
historicalFragmentsButton.onclick = ev => {sendSignal('/historical-fragments')};
objectButton.onclick = ev => {sendSignal('/object')};
worldDataButton.onclick = ev => {sendSignal('/world-data')};
console.log('listening')

function writeTable(response, endpoint){
    let addButtonArea = document.getElementById('add-one-button')
    addButtonArea.innerHTML = ''
    addButtonArea.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" id="add-item" fill="currentColor" class="bi bi-plus-circle" viewBox="0 0 16 16">
        <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
        <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4"/>
    </svg>`
    let addButton = document.getElementById('add-item')
    addButton.onclick = ev => {console.log('add somethin')} // Button will bring up form to fill out for the table. Query for data needed??
    let displayArea = document.getElementById('object-display')
    displayArea.innerHTML = ''
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
        let idClean = values[1]
        idClean = idClean.split(' ').join('')
        tableHTML += `<td><button id='${values[0]}-${idClean}'>${values[0]}</button></td>`
        for (let j = 1;j<values.length;j++){
            tableHTML += `<td>${values[j]}</td>`
        }
        tableHTML += `</tr>`
        // displayArea.html += tableHTML
        // console.log(`${values[0]}-${values[1]}`)
        // document.getElementById(`${values[0]}-${values[1]}`).onclick = () => console.log(`${endpoint}/?id=${values[0]}`)
    }
    tableHTML += `</table>`
    displayArea.innerHTML = tableHTML
    displayArea.innerHTML += '</div>'
    for (let i = 0;i<response.data.length;i++){
        let values = Object.values(response.data[i])
        // console.log(`${values[0]}-${values[1]}`)
        let idClean = values[1].split(' ').join('')
        let buttonTemp = document.getElementById(`${values[0]}-${idClean}`)
        console.log(buttonTemp)
        buttonTemp.onclick = ev => {
            sendOneSignal(`${endpoint}/?id=${values[0]}`)
        }
    }
}
function writeOne(data) {
    let singleDisplay = document.getElementById('single-display')
    singleDisplay.innerHTML = '';
    let { overview, traits, related } = data
    // console.log(overview)
    singleDisplay.innerHTML += '<h2>Overview</h2><ul>'
    for (const property in overview) {
        singleDisplay.innerHTML += `<li><b>${formatNormal(property)}:</b> ${overview[property]}</li>`
    }
    singleDisplay.innerHTML += '</ul>'
    singleDisplay.innerHTML += '<h2>Traits</h2>'
    for (const property in traits) {
        singleDisplay.innerHTML += `<h3>${formatNormal(property)}</h3><ul>`
        let currentTrait = traits[property] // this is where we'll ask for a name to make a card?
        for (let i = 0;i<currentTrait.length;i++) {
            let currentItem = currentTrait[i]
            for (const j in currentItem) {
                singleDisplay.innerHTML += `<li><b>${formatNormal(j)}:</b> ${currentItem[j]}</li>`
            }
        }
        singleDisplay.innerHTML += `</ul>`
    }
    singleDisplay.innerHTML += '<h2>Related</h2><ul>'
    // console.log(related)
    for (const property in related) {
        singleDisplay.innerHTML += `<h3>${formatNormal(property)}</h3><ul>`
        let currentProperty = related[property] //this is where we'll ask for an event name to make the card
        for (const i in currentProperty) {
            let currentItem = currentProperty[i]
            for (const j in currentItem) {
                singleDisplay.innerHTML += `<li><b>${formatNormal(j)}:</b> ${currentItem[j]}</li>`
            }
        }
        singleDisplay.innerHTML += `</ul>`
    }
    // console.log(relatedValues)
}
function sendOneSignal(endpoint) {
    const dmdmsconn = "http://127.0.0.1:8000";
    console.log(endpoint)
    axios.get(dmdmsconn + endpoint)
        .then((response) => writeOne(response.data))
        .catch((error) => console.log(error))
}
function sendSignal(endpoint) {
    const dmdmsconn = "http://127.0.0.1:8000";
    console.log(endpoint)
    axios.get(dmdmsconn + endpoint)
        .then((response) => writeTable(response, endpoint))
        .catch((error) => console.log(error))
}

function formatNormal(string) {
    let stringArr = string.split('_')
    let formattedArr = []
    for (let i = 0;i<stringArr.length;i++) {
        let word = stringArr[i]
        word = word[0].toUpperCase() + word.slice(1).toLowerCase()
        formattedArr.push(word)
    }
    return formattedArr.join(' ')
}
