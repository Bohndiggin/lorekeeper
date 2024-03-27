let actorButton = document.getElementById('actor-btn')
let factionButton = document.getElementById('faction-btn')
let locationButton = document.getElementById('location-btn')
let historyButton = document.getElementById('history-btn')
let objectButton = document.getElementById('object-btn')
let worldDataButton = document.getElementById('world-data-btn')
actorButton.onclick = ev => {sendSignal('/actor')};
factionButton.onclick = ev => {sendSignal('/faction')};
locationButton.onclick = ev => {sendSignal('/location')};
historyButton.onclick = ev => {sendSignal('/history')};
objectButton.onclick = ev => {sendSignal('/object')};
worldDataButton.onclick = ev => {sendSignal('/world-data')};

let currentOpen = {
    'table': '',
    'item': 0,
    'connective_table': ''
}

let openTableRows = {}

let orderDataDict = {}

function saveOrderData(data) {
    // console.log(data)
    let orderData = Papa.parse(data)
    let orderDataDictWork = {}
    for(let i = 1;i<orderData.data.length;i++) {
        // console.log(orderData.data[i])
        orderDataDictWork[orderData.data[i][0]] = []
        // console.log(orderDataDict)
        for(let j = 1;j<orderData.data[i].length;j++) {
            if (orderData.data[i][j] == '') {
                continue
            }
            // console.log(orderData.data[i][j])
            orderDataDictWork[orderData.data[i][0]].push(orderData.data[i][j])
        }
    }
    orderDataDict = orderDataDictWork
    console.log('orderDataDict Loaded')
    console.log(orderDataDict)
}

async function loadOrderData() {
    fetch('/main/properorders.csv')
        .then(response => response.text())
        .then((data) => saveOrderData(data))
        .catch(error => console.log(error))
}



let relationMap = {
    '/actor': {
        'faction_members': '/faction-names',
        'residents': '/location-names',
        'history_actor': '/history-names'
    },
    '/faction': {
        'faction_members': '/actor-names',
        'location_to_faction': '/location-names'
    },
    '/location': {
        'location_to_faction': '/faction-names',
        'residents': '/actor-names',
        'history_location': '/history-names'
    },
    '/history': {
        'history_actor': '/actor-names',
        'history_faction': '/faction-names',
        'history_location': '/location-names',
        'history_object': '/object-names',
        'history_world_data': '/world-data-names'
    },
    '/object': {
        'history_object': '/history-names',
        'object_to_owner': '/actor-names'
    },
    '/world-data': {
        'history_world_data': '/history-names'
    }
}

let tableData = {}

console.log('listening')

function writeTable(response, endpoint){
    let addButtonArea = document.getElementById('add-one-button')
    openTableRows = response.data
    console.log(openTableRows)
    addButtonArea.innerHTML = ''
    currentOpen['table'] = endpoint
    addButtonArea.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" id="add-item" fill="currentColor" class="bi bi-plus-circle" viewBox="0 0 16 16">
        <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
        <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4"/>
    </svg>`
    let addButton = document.getElementById('add-item')
    addButton.onclick = ev => {addButtonTopFunction()} // Button will bring up form to fill out for the table. Query for data needed??
    let displayArea = document.getElementById('object-display')
    displayArea.innerHTML = ''
    let keys = Object.keys(response.data[0])
    let tableHTML = `<table><tr>`
    for (let j = 0;j<keys.length;j++) {
        tableHTML += `<th>${keys[j]}</th>`
    }
    tableHTML += `</tr>`
    for (let i = 0;i<response.data.length;i++) {
        let values = Object.values(response.data[i])
        tableHTML += `<tr>`
        let idClean = values[1]
        idClean = idClean.split(' ').join('').replace('"', '').replace(`'`, '')
        tableHTML += `<td><button id='${values[0]}-${idClean}'>${values[0]}</button></td>`
        for (let j = 1;j<values.length;j++){
            tableHTML += `<td>${values[j]}</td>`
        }
        tableHTML += `</tr>`
    }
    tableHTML += `</table>`
    displayArea.innerHTML = tableHTML
    displayArea.innerHTML += '</div>'
    for (let i = 0;i<response.data.length;i++){
        let values = Object.values(response.data[i])
        let idClean = values[1].split(' ').join('').replace('"', '').replace(`'`, '')
        let buttonTemp = document.getElementById(`${values[0]}-${idClean}`)
        let idNum = values[0]
        buttonTemp.onclick = ev => {
            sendOneSignal(`${endpoint}/?id=${idNum}`, idNum)
        }
    }
}
function writeOne(data, idNum) {
    console.log(idNum)
    currentOpen['item'] = idNum
    let singleDisplay = document.getElementById('single-display')
    singleDisplay.innerHTML = '';
    let { overview, traits, related } = data
    singleDisplay.innerHTML += `<h2>Overview</h2><ul>`
    for (const property in overview) {
        singleDisplay.innerHTML += `<li><b>${formatNormal(property)}:</b> ${overview[property]}</li>`
    }
    singleDisplay.innerHTML += `</ul><div id='edit-${idNum}' class='add-btn-centered'></div>`
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
        addRelatedPropertyTemp.onclick = ev => {
            currentOpen['connective_table'] = property
            let tableNameTarget = property + "_table"
            tableNameTarget = tableNameTarget.replace('__', '_')
            popupBuilderArbiter(tableNameTarget, null)
        }
    }
    let editButton = document.getElementById(`edit-${idNum}`)
    editButton.onclick = event => {
        let tempTable = currentOpen['table'].slice(1) + '_table'
        tempTable = tempTable.replace('__', '_')
        let tempTarget = 0
        for (let i = 0;i<openTableRows.length;i++) {
            if (openTableRows[i].id == idNum) {
                tempTarget = i
            }
        }
        console.log("TEMP TARGET: " + tempTarget)
        popupBuilderArbiter(tempTable, tempTarget) // BROKEN NEEDS TO HAVE actual ID not row on page
    }
}
function sendOneSignal(endpoint, idNum) {
    const dmdmsconn = "";
    axios.get(dmdmsconn + endpoint)
        .then((response) => writeOne(response.data, idNum))
        .catch((error) => console.log(error))
}
function sendSignal(endpoint) {
    let singleDisplay = document.getElementById('single-display')
    singleDisplay.innerHTML = '';
    const dmdmsconn = "";
    axios.get(dmdmsconn + endpoint)
        .then((response) => {
            writeTable(response, endpoint)
        })
        .catch((error) => console.log(error))
}

function writePopup(response, currentWork) {
    let popUpWindow = document.getElementById('popup')
    popUpWindow.innerHTML = ``
    let listOfNames = response.data
    for (let i = 0;i<listOfNames.length;i++) {
        currentWork += `<option value='${listOfNames[i].id}'>${listOfNames[i].proper_name}</option>`
    }
    currentWork += `</div>`
    currentWork += `</select><button class='popup' id='submit-to-table'>Submit</button>`
    popUpWindow.innerHTML = currentWork
    //console.log(currentWork) //TODO add button to popup and be sure to pass along the id of the current selected so we can get the right thing added to the right table
    let submitButton = document.getElementById('submit-to-table')
    //console.log(submitButton)
    submitButton.onclick = ev => {
        let selectionBox = document.getElementById('selection')
        postToConnectiveTable(selectionBox.value)
    }
    let popupBackground = document.getElementById('popupbkg')
    popupBackground.onclick = ev => {
        // console.log('click')
        closeAddingWindow()
    }
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

function closeAddingWindow() {
    let popUpWindow = document.getElementById('popup')
    popUpWindow.innerHTML = ``
}

function postToConnectiveTable(selectedID) { // TODO Add function to server.py that returns a list of traits that are tracked in pgsql so we can gather them.
    const loreconn = "";
    let postData = {
        'currentOpen': currentOpen,
        'selectedId': selectedID
    }
    axios.post(loreconn + '/test-data-post', postData)
        .then(response => {
            // console.log(response)
        })
        .catch((error) => console.log(error))
}

function dropdownBuilder(htmlString, dataList, dataName) {
    htmlString += `<label for="${dataName}">${formatNormal(dataName)}:</label>`
    htmlString += `<select name="${dataName}" id="selection-${dataName}">`
    // console.log(dataList)
    for (let i = 0;i<dataList.length;i++) {
        htmlString += `<option value='${dataList[i].id}'>${dataList[i].proper_name}</option>`
    }
    htmlString += `</select>`
    return htmlString
}

function storeTables(dict) {
    tableData = dict.data
    console.log('TABLE DATA LOADED')
    console.log(tableData)
}

function loadTables() {
    const loreconn = "";
    console.log('Loading Table Data') //TODO Insert Loading bar
    axios.get(loreconn + '/load-tables')
        .then((response) => {
            storeTables(response)
        })
        .catch((error) => console.log(error))

}

async function getEndcapData(key) {
    const loreconn = "";
    let targetTable = key.slice(0, key.length -3) + '_table'
    // console.log(typeof(targetTable))
    let GetEndcapDataRequest = {
        'targetEndcap': targetTable
    }
    // console.log(GetEndcapDataRequest)
    return await axios.post(loreconn + '/query-endcaps', GetEndcapDataRequest)
        .then(response => {
            return response.data;
        })
        .catch(error => console.log(error.response))
}

async function getConnectiveData(key) {
    const loreconn = "";
    let endpoint = relationMap[currentOpen['table']][currentOpen['connective_table']];
    return await axios.get(loreconn + endpoint)
        .then(data => {return data})
        .catch(err => console.log(err))
}

function inputBoxBuilder(dataNameStr, initialValue) {
    let htmlString = `<label for="${dataNameStr}">${formatNormal(dataNameStr)}</label>`
    htmlString += `<input type="text" id="${dataNameStr}-input" placeholder='${dataNameStr}' value='${initialValue}'/>`
    return htmlString
}

function inputBoxBuilderNum(dataNameStr, initialValue) {
    let htmlString = `<label for="${dataNameStr}">${formatNormal(dataNameStr)}</label>`
    htmlString += `<input type="number" id="${dataNameStr}-input" placeholder='${dataNameStr}' value='${initialValue}'/>`
    return htmlString
}
async function queryConnectiveAndEndcap(value) {}


async function extraDataQuerier(currentRequested, itemNum) {
    let htmlWork = ``
    for (const [key, value] of Object.entries(currentRequested['foreign_keyed'])) {
        if (value[1] == 'id') {
            continue
        }
        if (!value[1].includes('_id')) {
            console.log('wabba')
            let returnedData = await getConnectiveData(value[1]).then(data => {return data})
            htmlWork += dropdownBuilder('', returnedData.data, value[1])
        } else if (value[1] != currentOpen['table'].slice(1) + '_id') {
            let returnedData = await getEndcapData(value[1]).then(data => {return data})
            htmlWork += dropdownBuilder('', returnedData, value[1])
        }
    }
    return htmlWork
}


async function popupBuilderArbiter(tableSelected, itemNum) {
    console.log('ITEM NUM' + itemNum)
    tableSelected = tableSelected.replace('-', '_')
    let popUpWindow = document.getElementById('popup')
    let currentRequested = tableData[tableSelected]
    console.log(tableSelected)
    console.log(currentRequested)
    htmlString = `
    <div class="popup", id='popupbkg'>
    </div>
    <div class="popup", id='popupbkg2'>
        <div class="popup" id="popup-window">
            <div class="popup" id="popup-content">
                <h2>Add/Edit</h2>
                <form class="popup right" id='popup-right'>
    `
    try {
        let listKeys = []
        for (const [key, value] of Object.entries(currentRequested['non_foreign'])) { //refactor to make it build number input boxes
            console.log(key)
            listKeys.push(key)
        }
        listKeys = sortIt(orderDataDict[tableSelected], listKeys)
        for (const key in listKeys) {
            if (key.includes('_id')) {
                continue
            }
            if (currentRequested['non_foreign'][key] == 'integer') {
                if (itemNum == null) {
                    htmlString += inputBoxBuilderNum(key, 0)
                    continue
                } else {
                    htmlString += inputBoxBuilderNum(key, openTableRows[itemNum][key]) // LOOK UP What num is supposed to be
                }
            }
            if (itemNum == null) {
                htmlString += inputBoxBuilder(key, key)
                continue
            } else {
                htmlString += inputBoxBuilder(key, openTableRows[itemNum][key])
            }
        }
    } catch (error) {
        console.log(error)
    }
    try {
        htmlString += await extraDataQuerier(currentRequested, itemNum)
    } catch (error) {
        console.log(error)
    }


    htmlString += `<input type='submit' id='popup-submit' value='Submit'></form></div></div></div>`
    popUpWindow.innerHTML = htmlString
    // let submitButtonPopup = document.getElementById('popup-submit')
    // submitButtonPopup.onclick = ev => {
    //     getForm()
    // }
    let popupBackground = document.getElementById('popupbkg')
    popupBackground.onclick = ev => {
        closeAddingWindow()
    }
    let form = document.getElementById('popup-right')
    let formData = {}
    form.addEventListener('submit', event => {
        event.preventDefault()
        console.log(itemNum)
        //loop through and get values of all strings
        for (const [key, value] of Object.entries(currentRequested['non_foreign'])) {
            if (key.includes('_id')){
                continue
            }
            formData[key] = document.getElementById(key + '-input').value
        }
        for (const [key, value] of Object.entries(currentRequested['foreign_keyed'])) {
            if (key == 'id') {
                continue
            }
            if (key == currentOpen['table'].replace('/', '').replace('_table', '') + '_id') {
                console.log('key found')
                formData[key] = currentOpen['item']
                continue
            }
            // console.log(key)
            formData[key] = parseInt(document.getElementById('selection-' + key).value)
        }
        const loreconn = "/";
        console.log(formData)
        let targetEndpoint = tableSelected.replace('_table', '')
        if (itemNum == null) {
            axios.post(loreconn + targetEndpoint, data=formData)
            .then(response => {
            console.log(response)
            })
            .catch(error => {
                console.log(error)
            });
        } else {
            formData['id'] = itemNum
            axios.put(loreconn + targetEndpoint, data=formData)
            .then(response => {
                console.log(response)
            })
            .catch(error => {
                console.log(error)
            })
        }
        sendSignal(currentOpen['table'])
            closeAddingWindow()
        })
    return htmlString
}

function addButtonTopFunction() {
    let table = currentOpen['table'].slice(1) + '_table'
    table = table.replace('__', '_')
    popupBuilderArbiter(table, null)
}

function sortIt(orderedExampleList, toSortList) {

    result = {}
    for (let i =0;i<orderedExampleList.length;i++) {
        result[orderedExampleList[i]] = toSortList[toSortList.indexOf(orderedExampleList[i])]
    }
    return result
}
loadOrderData()
loadTables()

sendSignal('/actor')
