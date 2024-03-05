// const { response } = require("express")

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

let currentOpen = {
    'table': '',
    'item': 0,
    'connective_table': ''
}

let relationMap = {
    '/actor': {
        'faction_members': '/faction-names',
        'residents': '/location-names',
        'involved_history_actor': '/historical-fragments-names'
    },
    '/faction': {
        'faction_members': '/actor-names',
        'location_to_faction': '/location-names'
    },
    '/location': {
        'location_to_faction': '/faction-names',
        'residents': '/actor-names',
        'involved_history_location': '/historical-fragments-names'
    },
    '/historical-fragments': {
        'involved_history_actor': '/actor-names',
        'involved_history_faction': '/faction-names',
        'involved_history_location': '/location-names',
        'involved_history_object': '/object-names',
        'involved_history_world_data': '/world-data-names'
    },
    '/object': {
        'involved_history_object': '/historical-fragments-names',
        'object_to_owner': '/actor-names'
    },
    '/world-data': {
        'involved_history_world_data': '/historical-fragments-names'
    }
}

let tableData = {}

console.log('listening')

function writeTable(response, endpoint){
    let addButtonArea = document.getElementById('add-one-button')
    addButtonArea.innerHTML = ''
    currentOpen['table'] = endpoint
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
        let idNum = values[0]
        buttonTemp.onclick = ev => {
            sendOneSignal(`${endpoint}/?id=${idNum}`, idNum)
        }
    }
}
function writeOne(data, idNum) {
    currentOpen['item'] = idNum
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
        singleDisplay.innerHTML += `</ul><div id="add-${property}" class='add-btn-centered'><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-circle add-btn-centered" viewBox="0 0 16 16">
        <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
        <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4"/>
        </svg></div>`
    }
    for (const property in related) {
        let addRelatedPropertyTemp = document.getElementById(`add-${property}`)
        console.log(addRelatedPropertyTemp)
        addRelatedPropertyTemp.onclick = ev => {
            openAddingWindow(property)
        }
    }
    // console.log(relatedValues)
}
function sendOneSignal(endpoint, idNum) {
    const dmdmsconn = "http://127.0.0.1:8000";
    console.log(endpoint)
    axios.get(dmdmsconn + endpoint)
        .then((response) => writeOne(response.data, idNum))
        .catch((error) => console.log(error))
}
function sendSignal(endpoint) {
    let singleDisplay = document.getElementById('single-display')
    singleDisplay.innerHTML = '';
    const dmdmsconn = "http://127.0.0.1:8000";
    console.log(endpoint)
    axios.get(dmdmsconn + endpoint)
        .then((response) => writeTable(response, endpoint))
        .catch((error) => console.log(error))
}

function writePopup(response, currentWork) {
    let popUpWindow = document.getElementById('popup')
    popUpWindow.innerHTML = ``
    let listOfNames = response.data
    console.log(listOfNames)
    for (let i = 0;i<listOfNames.length;i++) {
        currentWork += `<option value='${listOfNames[i].id}'>${listOfNames[i].proper_name}</option>`
    }
    currentWork += `</div>`
    currentWork += `</select><button class='popup' id='submit-to-table'>Submit</button>`
    popUpWindow.innerHTML = currentWork
    console.log(currentWork) //TODO add button to popup and be sure to pass along the id of the current selected so we can get the right thing added to the right table
    let submitButton = document.getElementById('submit-to-table')
    console.log(submitButton)
    submitButton.onclick = ev => {
        let selectionBox = document.getElementById('selection')
        postToConnectiveTable(selectionBox.value)
    }
    let popupBackground = document.getElementById('popupbkg')
    popupBackground.onclick = ev => {
        console.log('click')
        closeAddingWindow()
    }
}

function populateDropDown(currentWork) { //Function queries for the proper names for everything in a table to populate dropdown menus
    // console.log("currentTable: " + currentTable);
    const dmdmsconn = "http://127.0.0.1:8000";
    endpoint = relationMap[currentOpen['table']][currentOpen['connective_table']]
    console.log('ENDPOINT ' + endpoint)
    axios.get(dmdmsconn + endpoint)
        .then((response) => {
            writePopup(response, currentWork)
        })
        .catch((error) => console.log(error))
};

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

function openAddingWindow(connTable) {// TODO add function to write dropdown/inputs based on the return of the previous function
    currentOpen['connective_table'] = connTable
    let popUpWindow = document.getElementById('popup')
    popUpWindow.innerHTML = ``
    let popUpWindowBuild = `
    <div class="popup", id='popupbkg'>
    </div>
    <div class="popup", id='popupbkg2'>
        <div class="popup" id="popup-window">
            <div class="popup" id="popup-content">
                <h2>CONNECT TO</h2>
                <div class="popup right" id='popup-right'>
                    <label for="selection">Join with:</label>
    `
    popUpWindowBuild += `<select name="selection" id="selection">`
    populateDropDown(popUpWindowBuild)
}

function closeAddingWindow() {
    let popUpWindow = document.getElementById('popup')
    popUpWindow.innerHTML = ``
}

function postToConnectiveTable(selectedID) { // TODO Add function to server.py that returns a list of traits that are tracked in pgsql so we can gather them.
    const loreconn = "http://127.0.0.1:8000";
    let postData = {
        'currentOpen': currentOpen,
        'selectedId': selectedID
    }
    axios.post(loreconn + '/test-data-post', postData)
        .then(response => {
            console.log(response)
        })
        .catch((error) => console.log(error))
}

function dropdownBuilder(htmlString, dataList, dataName) {
    // htmlString += `<label for="selection">Join with:</label>`
    htmlString += `<select name="selection" id="selection-${dataName}">`
    for (const item in dataList) {
        htmlString += `<option value='${item.id}'>${item.proper_name}</option>`
    }
    htmlString += `</select>`
    return htmlString
}

function storeTables(dict) {
    tableData = dict.data
    console.log('TABLE DATA STORED')
    console.log(tableData)
}

function loadTables() {
    const loreconn = "http://127.0.0.1:8000";
    axios.get(loreconn + '/load-tables')
        .then((response) => {
            console.log('Loading Table Data') //TODO Insert Loading bar
            storeTables(response)
        })
        .catch((error) => console.log(error))

}

function inputBoxBuilder(htmlString, tableIdStr, dataNameStr, dataType) {
    htmlString += `<label>${dataNameStr}</label>`
}

function popupBuilderArbiter(formDataNeeded) {
    
}

loadTables()