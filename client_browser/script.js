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

let openTableRows = {}

let orderDataDict = {}

let openItemData = {}

let tablesObjects = {}

let openTableObject = {}

let relationMap = {
    '/actor': {
        'faction_members': '/faction-names',
        'residents': '/location-names',
        'history_actor': '/history-names'
    },
    'actor': {
        'faction_members': '/faction-names',
        'residents': '/location-names',
        'history_actor': '/history-names'
    },
    '/faction': {
        'faction_members': '/actor-names',
        'location_to_faction': '/location-names'
    },
    'faction': {
        'faction_members': '/actor-names',
        'location_to_faction': '/location-names'
    },
    '/location': {
        'location_to_faction': '/faction-names',
        'residents': '/actor-names',
        'history_location': '/history-names'
    },
    'location': {
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
    'history': {
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
    'object': {
        'history_object': '/history-names',
        'object_to_owner': '/actor-names'
    },
    '/world-data': {
        'history_world_data': '/history-names'
    },
    'world_data': {
        'history_world_data': '/history-names'
    }
}

class PgTable {
    constructor(tableNameTable, tableDataTemp) {
        this.tableNameTable = tableNameTable
        this.tableName = tableNameTable.replace('_table', '')
        this.tableKeys = this.getTableKeys(tableDataTemp)
        this.tableOrder = this.getTableOrder()
        this.tableRelations = this.getTableRelations()
        this.tableEndpoint = '/' + this.tableName
        this.tableEndpoint = this.tableEndpoint.replace('_', '-')
        this.rows = new Set();
    }

    getTableKeys(tableDataTemp) {
        return tableDataTemp[this.tableNameTable]
    }

    getTableOrder() {
        return orderDataDict[this.tableNameTable]
    }

    getTableRelations() {
        return relationMap[this.tableName]
    }

    addRow(row) {
        if (!this.getRow(row.id)) {
            this.rows.add(row)
        }
    }

    getRelation(tableName) {
        return "name of relation-names"
    }

    getRow(rowIdNum) {
        let tempIter = this.rows.values()
        for(let i = 0;i<this.rows.size;i++) {
            let tempCheck = tempIter.next().value
            if (tempCheck.id == rowIdNum) {
                return tempCheck
            }
        }
        return null
    }
}

async function saveOrderData(data) {
    let orderData = Papa.parse(data)
    let orderDataDictWork = {}
    for(let i = 1;i<orderData.data.length;i++) {
        orderDataDictWork[orderData.data[i][0]] = []
        for(let j = 1;j<orderData.data[i].length;j++) {
            if (orderData.data[i][j] == '') {
                continue
            }
            orderDataDictWork[orderData.data[i][0]].push(orderData.data[i][j])
        }
    }
    console.log('orderDataDict Loaded')
    return orderDataDictWork
}

async function loadOrderData() {
    fetch('/main/properorders.csv')
    .then(response => response.text())
    .then((data) => saveOrderData(data))
    .catch(error => console.log(error))
}

async function storeTables(dict) {
    let tableDataTemp = dict.data
    console.log('TABLE DATA LOADED')
    let tablesObjectsTemp = {}
    for (const [key, value] of Object.entries(tableDataTemp)) {
        tablesObjectsTemp[key.replace('_table', '')] = new PgTable(key, tableDataTemp)
    }
    return tablesObjectsTemp
}

async function loadTables() {
    const loreconn = "";
    console.log('Loading Table Data') //TODO Insert Loading bar
    return await axios.get(loreconn + '/load-tables')
    .then((response) => {
        return storeTables(response)
    })
    .catch((error) => console.log(error))
}

async function load() {
    try {
        const response = await fetch('/main/properorders.csv');
        const data = await response.text();
        orderDataDict = await saveOrderData(data);
        tablesObjects = await loadTables();
        console.log(tablesObjects)
        sendSignal('/actor');
    } catch (error) {
        console.log(error);
    }
}

console.log('listening')

// LISTENING

function writeTable(response, endpoint){
    let addButtonArea = document.getElementById('add-one-button')
    let endpointClean = endpoint.replace('-', '_').replace('/', '')
    openTableObject = tablesObjects[endpointClean]
    openTableRows = response.data
    addButtonArea.innerHTML = ''
    addButtonArea.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" id="add-item" fill="currentColor" class="bi bi-plus-circle" viewBox="0 0 16 16">
        <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
        <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4"/>
    </svg>`
    let addButton = document.getElementById('add-item')
    addButton.onclick = ev => {addButtonTopFunction()} // Button will bring up form to fill out for the table. Query for data needed??
    let displayArea = document.getElementById('object-display')
    displayArea.innerHTML = ''
    // openTableObject.rows = []
    for (let i = 0;i<response.data.length;i++) {
        openTableObject.addRow(response.data[i])
    }
    let tableHTML = `<table id="myTable" class="display"><tr><thead>`
    tableHTML += `<th>id</th>`
    for (let i = 0;i<openTableObject.tableOrder.length;i++) {
        tableHTML += `<th>${openTableObject.tableOrder[i]}</th>`
    }
    tableHTML += `</tr></thead><tbody>`
    let rowIter = openTableObject.rows.values()
    for (let i = 0;i<openTableObject.rows.size;i++) {
        let currentRow = rowIter.next().value
        tableHTML += `<tr>`
        tableHTML += `<td><button id='${currentRow.id}-select-one'>${currentRow.id}</button></td>`
        for (let j = 0;j<openTableObject.tableOrder.length;j++){
            tableHTML += `<td>${currentRow[openTableObject.tableOrder[j]]}</td>`
        }
        tableHTML += `</tr>`
    }
    tableHTML += `</tbody></table>`
    tableHTML += '</div>'
    displayArea.innerHTML = tableHTML
    let rowIter2 = openTableObject.rows.values()
    for (let i = 0;i<openTableObject.rows.size;i++){
        let currentRow = rowIter2.next().value
        let idNum = currentRow.id
        let buttonTemp = document.getElementById(`${idNum}-select-one`)
        buttonTemp.onclick = ev => {
            sendOneSignal(`${endpoint}/?id=${idNum}`, idNum)
        }
    }
}
function writeOne(data, idNum) {
    let singleDisplay = document.getElementById('single-display')
    singleDisplay.innerHTML = '';
    openItemData = data
    let currentRow = openTableObject.getRow(idNum)
    let { selfConnective, traits, related } = data
    let tempHTML = ``
    // OVERVIEW
    tempHTML += `<h2>Overview</h2><ul>`
    for (let i = 0;i<openTableObject.tableOrder.length;i++) {
        let tempProperty = openTableObject.tableOrder[i]
        tempHTML += `<li><b>${formatNormal(tempProperty)}: </b> ${currentRow[tempProperty]}</li>`
    }
    tempHTML += `<div id='edit-${idNum}' class='edit-btn-centered'><svg fill="#000000" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="64px" height="64px" viewBox="0 0 494.936 494.936" xml:space="preserve"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <g> <g> <path d="M389.844,182.85c-6.743,0-12.21,5.467-12.21,12.21v222.968c0,23.562-19.174,42.735-42.736,42.735H67.157 c-23.562,0-42.736-19.174-42.736-42.735V150.285c0-23.562,19.174-42.735,42.736-42.735h267.741c6.743,0,12.21-5.467,12.21-12.21 s-5.467-12.21-12.21-12.21H67.157C30.126,83.13,0,113.255,0,150.285v267.743c0,37.029,30.126,67.155,67.157,67.155h267.741 c37.03,0,67.156-30.126,67.156-67.155V195.061C402.054,188.318,396.587,182.85,389.844,182.85z"></path> <path d="M483.876,20.791c-14.72-14.72-38.669-14.714-53.377,0L221.352,229.944c-0.28,0.28-3.434,3.559-4.251,5.396l-28.963,65.069 c-2.057,4.619-1.056,10.027,2.521,13.6c2.337,2.336,5.461,3.576,8.639,3.576c1.675,0,3.362-0.346,4.96-1.057l65.07-28.963 c1.83-0.815,5.114-3.97,5.396-4.25L483.876,74.169c7.131-7.131,11.06-16.61,11.06-26.692 C494.936,37.396,491.007,27.915,483.876,20.791z M466.61,56.897L257.457,266.05c-0.035,0.036-0.055,0.078-0.089,0.107 l-33.989,15.131L238.51,247.3c0.03-0.036,0.071-0.055,0.107-0.09L447.765,38.058c5.038-5.039,13.819-5.033,18.846,0.005 c2.518,2.51,3.905,5.855,3.905,9.414C470.516,51.036,469.127,54.38,466.61,56.897z"></path> </g> </g> </g></svg></div></ul>`
    // TRAITS
    tempHTML += '<h2>Traits</h2><ul>'
    let workingTableObject = null
    for (const [trait, traitList] of Object.entries(traits)) {
        tablesObjects[trait].addRow(traitList)
        workingTableObject = tablesObjects[trait]
        tempHTML += `<h3>${formatNormal(trait)}</h3><ul>`
        for (let i = 0;i<traitList.length;i++){
            for (const traitName of workingTableObject.tableOrder) {
                tempHTML += `<li><b>${formatNormal(traitName)}:</b> ${traitList[i][traitName]}</li>`
            }
        }
        tempHTML += `</ul>`
    }
    tempHTML += `</ul>`
    // RELATED
    tempHTML += '<h2>Related</h2><ul>'
    // SELF- CONNECTIVE
    for (const [trait, traitList] of Object.entries(selfConnective)) {
        workingTableObject = tablesObjects[trait]
        tempHTML += `<h3>${formatNormal(trait)}</h3><ul>`
        for (let i = 0;i<traitList.length;i++){
            for (const traitName of workingTableObject.tableOrder) {
                tempHTML += `<li><b>${formatNormal(traitName)}:</b> ${traitList[i][traitName]}</li>`
            }
        }
        tempHTML += `<br>`
        tempHTML += `</ul><div id="add-${trait}" class='add-btn-centered'><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-circle add-btn-centered" viewBox="0 0 16 16">
        <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
        <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4"/>
        </svg></div>`
        tempHTML += `</ul>`
    }
    //RELATED
    for (const [trait, traitList] of Object.entries(related)) {
        workingTableObject = tablesObjects[trait]
        tempHTML += `<h3 id='${trait}-list'>${formatNormal(trait)}</h3><ul>`
        for (let i = 0;i<traitList.length;i++){
            workingTableObject.addRow(traitList[i])
            for (const traitName of workingTableObject.tableOrder) {
                tempHTML += `<li id='${trait}-${i}-${traitName}-list'><b>${formatNormal(traitName)}:</b> ${traitList[i][traitName]}</li>`
            }
            tempHTML += `<br>`
        }
        // tempHTML += `</ul>`
        tempHTML += `<div id="add-${trait}" class='add-btn-centered'><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-circle add-btn-centered" viewBox="0 0 16 16">
        <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
        <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4"/>
        </svg></div></ul>`
    }
    tempHTML += `</ul>`
    singleDisplay.innerHTML = tempHTML
    for (const [trait, traitList] of Object.entries(selfConnective)) {
        let addRelatedPropertyTemp = document.getElementById(`add-${trait}`)
        addRelatedPropertyTemp.onclick = ev => {
            popupBuilderArbiter(trait, null)
        }
    }
    for (const property in related) {
        let addRelatedPropertyTemp = document.getElementById(`add-${property}`)
        addRelatedPropertyTemp.onclick = ev => {
            popupBuilderArbiter(property, null)
        }
    }
    for (const [trait, traitList] of Object.entries(related)) {
        workingTableObject = tablesObjects[trait]
        for (let i = 0;i<traitList.length;i++){
            for (const traitName of workingTableObject.tableOrder) {
                let tempButton = document.getElementById(`${trait}-${i}-${traitName}-list`)
                tempButton.onclick = event => {
                    let currentRow = workingTableObject.getRow(traitList[i].id)
                    popupBuilderArbiter(trait, currentRow.id)
                }
            }
        }
    }
    let editButton = document.getElementById(`edit-${idNum}`)
    editButton.onclick = event => {
        popupBuilderArbiter(openTableObject.tableName, idNum)
    }
}
function sendOneSignal(endpoint, idNum) {
    axios.get(endpoint)
        .then((response) => writeOne(response.data, idNum))
        .catch((error) => console.log(error))
}
function sendSignal(endpoint) {
    let singleDisplay = document.getElementById('single-display')
    singleDisplay.innerHTML = '';
    axios.get(endpoint)
        .then((response) => {writeTable(response, endpoint)})
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

function closeAddingWindow() {
    let popUpWindow = document.getElementById('popup')
    popUpWindow.innerHTML = ``
}

function dropdownBuilder(htmlString, dataList, dataName, itemNum) {
    htmlString += `<label for="${dataName}">${formatNormal(dataName)}:</label>`
    htmlString += `<select name="${dataName}" id="selection-${dataName}">`
    for (let i = 0;i<dataList.length;i++) {
        htmlString += `<option value='${dataList[i].id}'>${dataList[i].proper_name}</option>`
    }
    htmlString += `</select>`
    return htmlString
}

async function getEndcapData(key) {
    let targetTable = key.slice(0, key.length -3) + '_table'
    let GetEndcapDataRequest = {
        'targetEnd': targetTable
    }
    return await axios.post('/query-ends', GetEndcapDataRequest)
        .then(response => {return response.data})
        .catch(error => console.log(error.response))
}

async function getSelfConnectiveData(key) {
    let cleanKey = key.replace('_b_', '_')
    console.log(cleanKey)
    let targetTable = cleanKey.replace('_id','_table').replace('__', '_')
    let GetSelfConnectiveDataRequest = {
        'targetSelfConnective': targetTable
    }
    return await axios.post('/query-self-connective', GetSelfConnectiveDataRequest)
        .then(response => {return response.data})
        .catch(error => console.log(error))
}

async function getConnectiveData(key) {
    let endpoint = relationMap[currentOpen['table_endpoint']][currentOpen['connective_table']];
    return await axios.get(loreconn + endpoint)
        .then(data => {return data})
        .catch(err => console.log(err))
}

function inputBoxBuilder(dataNameStr, initialValue) {
    let htmlString = `<label for="${dataNameStr}">${formatNormal(dataNameStr)}</label>`
    htmlString += `<input type="text" id="${dataNameStr}-input" placeholder='${dataNameStr}' value='${initialValue}'/>`
    return htmlString
}

function inputBoxBuilderNum(dataNameStr, initialValue, type) {
    let htmlString = `<label for="${dataNameStr}">${formatNormal(dataNameStr)} (${type}):</label>`
    htmlString += `<input type="number" id="${dataNameStr}-input" placeholder='${dataNameStr}' value='${initialValue}'/>`
    return htmlString
}

function inputBoxBuilderFloat(dataNameStr, initialValue, type) {
    let htmlString = `<label for="${dataNameStr}">${formatNormal(dataNameStr)} (${type}):</label>`
    htmlString += `<input type="range" step='0.01' id="${dataNameStr}-input" min="0" max="1" value='${initialValue}' oninput="this.nextElementSibling.value = this.value"/>`
    htmlString += `<output>${initialValue}</output>`
    return htmlString
}

async function queryConnectiveAndEndcap(value) {}

async function popupBuilderArbiter(tableSelected, itemNum) {
    let popUpWindow = document.getElementById('popup')
    let currentRequested = tablesObjects[tableSelected]
    console.log(currentRequested.tableKeys)
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
        for (let i = 0;i<currentRequested.tableOrder.length;i++) {
            let orderedKey = currentRequested.tableOrder[i]
            let targetKey = currentRequested.tableKeys[orderedKey]
            if (targetKey.foreign == 'false') {
                // non-foreign work
                if (targetKey.datatype == "INTEGER") {
                    if (itemNum == null) {
                        htmlString += inputBoxBuilderNum(targetKey.key_name, 0, targetKey.datatype)
                        continue
                    } else {
                        htmlString += inputBoxBuilderNum(targetKey.key_name, openTableObject.getRow(itemNum)[targetKey.key_name], targetKey.datatype)
                        continue
                    }
                }
                if (targetKey.datatype == "FLOAT") {
                    if (itemNum == null) {
                        htmlString += inputBoxBuilderFloat(targetKey.key_name, 0, targetKey.datatype)
                        continue
                    } else {
                        htmlString += inputBoxBuilderFloat(targetKey.key_name, openTableObject.getRow(itemNum)[targetKey.key_name], targetKey.datatype)
                        continue
                    }
                }
                if (itemNum == null) {
                    htmlString += inputBoxBuilder(targetKey.key_name, targetKey.key_name)
                    continue
                } else {
                    htmlString += inputBoxBuilder(targetKey.key_name, openTableObject.getRow(itemNum)[targetKey.key_name])
                    continue
                }
            } else {
                // foreign work
                if (!targetKey.key_name.includes('_id')) {
                    let returnedData = await getConnectiveData(targetKey.key_name).then(data => {return data})
                    htmlString += dropdownBuilder('', returnedData.data, targetKey.key_name)
                } else if (targetKey.key_name.includes('_b_')){
                    let returnedData = await getSelfConnectiveData(targetKey.key_name).then(data => {return data})
                    htmlString += dropdownBuilder('', returnedData, targetKey.key_name)
                } else if (targetKey.key_name.includes('_a_')) {
                    continue
                } else if (targetKey.key_name != openTableObject.tableName + '_id') {
                    let returnedData = await getEndcapData(targetKey.key_name).then(data => {return data})
                    htmlString += dropdownBuilder('', returnedData, targetKey.key_name, itemNum)
                }
            }
        }
    } catch (error) {
        console.log(error)
    }
    htmlString += `<br><br><input type='submit' id='popup-submit' value='Submit' id='popup-submit'></form></div></div></div><br><br>`
    popUpWindow.innerHTML = htmlString
    if (itemNum != null) {
        for (let i = 0;i<currentRequested.tableOrder.length;i++) {
            let orderedKey = currentRequested.tableOrder[i]
            let targetKey = currentRequested.tableKeys[orderedKey]
            if (targetKey.foreign == "true") {
                let tempSelection = document.getElementById('selection-' + targetKey.key_name)
                try {
                    tempSelection.selectedIndex = parseInt(openTableObject.getRow(itemNum)[targetKey.key_name]) - 1
                } catch (error) {
                    console.log(error)
                }
            }
        }
    }
    let popupBackground = document.getElementById('popupbkg')
    popupBackground.onclick = ev => {
        closeAddingWindow()
    }
    let form = document.getElementById('popup-right')
    let formData = {}
    form.addEventListener('submit', event => { // REWRITE TO account for ID not being the open item's id
        event.preventDefault()
        //loop through and get values of all strings
        formData['id'] = itemNum
        for (let i = 0;i<currentRequested.tableOrder.length;i++) {
            let orderedKey = currentRequested.tableOrder[i]
            let targetKey = currentRequested.tableKeys[orderedKey]
            let keyName = targetKey.key_name
            if (targetKey.foreign == 'true') {
                console.log(keyName)
                console.log(currentRequested.tableName + '_id')
                if (keyName == currentRequested.tableName + '_id') {
                    formData[keyName] = itemNum
                    continue
                } else if (keyName.includes('_a_')) {
                    formData[keyName] = itemNum
                    continue
                }
                let selectionValue = document.getElementById('selection-' + keyName).value
                formData[keyName] = parseInt(selectionValue)
            } else {
                formData[keyName] = document.getElementById(keyName + '-input').value
            }
            // formData[keyName] = document.getElementById(keyName + '-input').value
        }
        let targetEndpoint = currentRequested.tableEndpoint.replace('_table', '').replace(/_/g, '-')
        if (itemNum == null) {
            axios.post(targetEndpoint, data=formData)
            .then(response => {
            console.log(response)
            })
            .catch(error => {
                console.log(error)
            });
        } else {
            formData['id'] = itemNum
            axios.put(targetEndpoint, data=formData)
            .then(response => {
                console.log(response)
            })
            .catch(error => {
                console.log(error)
            })
        }
        sendSignal(openTableObject.tableEndpoint)
        closeAddingWindow()
        })
    return htmlString
}

function addButtonTopFunction() {
    popupBuilderArbiter(openTableObject.tableName, null)
}

load()
