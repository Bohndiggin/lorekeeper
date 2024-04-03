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
    'connective_table': '',
    'table_endpoint': ''
}

let openTableRows = {}

let orderDataDict = {}

// function cleanEscape(string) {
//     string = string.replace(' ', '')
//     string = string.replace('__', '_')
//     return string
// }

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
    addButtonArea.innerHTML = ''
    let tableDunder = endpoint.slice(1) + '_table'
    currentOpen['table'] = tableDunder.replace('__', '_').replace('-', '_')
    currentOpen['table_endpoint'] = endpoint
    addButtonArea.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" id="add-item" fill="currentColor" class="bi bi-plus-circle" viewBox="0 0 16 16">
        <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
        <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4"/>
    </svg>`
    let addButton = document.getElementById('add-item')
    addButton.onclick = ev => {addButtonTopFunction()} // Button will bring up form to fill out for the table. Query for data needed??
    let displayArea = document.getElementById('object-display')
    displayArea.innerHTML = ''
    let tablesSorted = []
    for (let i = 0;i<response.data.length;i++) {
        let tempRow = [['id', response.data[i]['id']]]
        tempRow = tempRow.concat(sortDictToList(orderDataDict[currentOpen['table']], response.data[i]))
        tablesSorted.push(tempRow)
    }
    let tableHTML = `<table id="myTable" class="display"><tr><thead>`
    for (let i = 0;i<tablesSorted[0].length;i++) {
        tableHTML += `<th>${tablesSorted[0][i][0]}</th>`
    }
    tableHTML += `</tr></thead><tbody>`
    for (let i = 0;i<tablesSorted.length;i++) {
        let values = tablesSorted[i]
        tableHTML += `<tr>`
        let idClean = values[1][1]
        tableHTML += `<td><button id='${values[0][1]}-${idClean}'>${values[0][1]}</button></td>`
        for (let j = 1;j<values.length;j++){
            tableHTML += `<td>${values[j][1]}</td>`
        }
        tableHTML += `</tr>`
    }
    tableHTML += `</tbody></table>`
    tableHTML += '</div>'
    displayArea.innerHTML = tableHTML
    for (let i = 0;i<tablesSorted.length;i++){
        let values = tablesSorted[i]
        let idClean = values[1][1]
        let buttonTemp = document.getElementById(`${values[0][1]}-${idClean}`)
        let idNum = values[0][1]
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
    let { overview, selfConnective, traits, related } = data
    overview = sortDictToList(orderDataDict[currentOpen['table']], overview)
    overview = listToDict(overview)
    let tempHTML = ``
    // OVERVIEW
    tempHTML += `<h2>Overview</h2><ul>`
    for (const property in overview) {
        tempHTML += `<li><b>${formatNormal(property)}:</b> ${overview[property]}</li>`
    }
    tempHTML += `<div id='edit-${idNum}' class='edit-btn-centered'><svg fill="#000000" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="64px" height="64px" viewBox="0 0 494.936 494.936" xml:space="preserve"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <g> <g> <path d="M389.844,182.85c-6.743,0-12.21,5.467-12.21,12.21v222.968c0,23.562-19.174,42.735-42.736,42.735H67.157 c-23.562,0-42.736-19.174-42.736-42.735V150.285c0-23.562,19.174-42.735,42.736-42.735h267.741c6.743,0,12.21-5.467,12.21-12.21 s-5.467-12.21-12.21-12.21H67.157C30.126,83.13,0,113.255,0,150.285v267.743c0,37.029,30.126,67.155,67.157,67.155h267.741 c37.03,0,67.156-30.126,67.156-67.155V195.061C402.054,188.318,396.587,182.85,389.844,182.85z"></path> <path d="M483.876,20.791c-14.72-14.72-38.669-14.714-53.377,0L221.352,229.944c-0.28,0.28-3.434,3.559-4.251,5.396l-28.963,65.069 c-2.057,4.619-1.056,10.027,2.521,13.6c2.337,2.336,5.461,3.576,8.639,3.576c1.675,0,3.362-0.346,4.96-1.057l65.07-28.963 c1.83-0.815,5.114-3.97,5.396-4.25L483.876,74.169c7.131-7.131,11.06-16.61,11.06-26.692 C494.936,37.396,491.007,27.915,483.876,20.791z M466.61,56.897L257.457,266.05c-0.035,0.036-0.055,0.078-0.089,0.107 l-33.989,15.131L238.51,247.3c0.03-0.036,0.071-0.055,0.107-0.09L447.765,38.058c5.038-5.039,13.819-5.033,18.846,0.005 c2.518,2.51,3.905,5.855,3.905,9.414C470.516,51.036,469.127,54.38,466.61,56.897z"></path> </g> </g> </g></svg></div></ul>`
    // TRAITS
    tempHTML += '<h2>Traits</h2><ul>'
    for (const property in traits) {
        tempHTML += `<h3>${formatNormal(property)}</h3><ul>`
        let currentTrait = traits[property] // this is where we'll ask for a name to make a card?
        let formattedProperty = property + '_table'
        for (let i = 0;i<currentTrait.length;i++) {
            let currentItem = currentTrait[i]
            // console.log(sortItToList(orderDataDict[formattedProperty], currentItem))
            for (let j = 0;j<orderDataDict[formattedProperty].length; j++) {
                tempHTML += `<li><b>${formatNormal(orderDataDict[formattedProperty][j])}:</b> ${currentItem[orderDataDict[formattedProperty][j]]}</li>`
            }
            tempHTML += `</ul>`
        }
    }
    tempHTML += `</ul>`
    // RELATED
    tempHTML += '<h2>Related</h2><ul>'
    // SELF- CONNECTIVE
    for (const property in selfConnective) {
        tempHTML += `<h3>${formatNormal(property)}</h3><ul>`
        let currentTrait = selfConnective[property] // this is where we'll ask for a name to make a card?
        console.log(currentTrait)
        let formattedProperty = property + '_table'
        for (let i = 0;i<currentTrait.length;i++) {
            let currentItem = currentTrait[i]
            for (const j in currentItem) {
                console.log(j)
                if (j.includes('_id')) {
                    console.log('id')
                    continue
                }
                tempHTML += `<li id='${property}-${j}'><b>${formatNormal(j)}:</b> ${currentItem[j]}</li>`
            }
        }
        tempHTML += `</ul>`
    }
    for (const property in related) {
        tempHTML += `<h3>${formatNormal(property)}</h3><ul>`
        let currentProperty = related[property] //this is where we'll ask for an event name to make the card
        for (const i in currentProperty) {
            let currentItem = currentProperty[i]
            let formattedProperty = property + '_table'
            for (const j in currentItem) {
                if (j.includes('id')) {
                    continue
                }
                tempHTML += `<li id='${property}-${j}'><b>${formatNormal(j)}:</b> ${currentItem[j]}</li>`
            }
            tempHTML += `<br>`
        }
        // tempHTML += `</ul>`
        tempHTML += `</ul><div id="add-${property}" class='add-btn-centered'><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-circle add-btn-centered" viewBox="0 0 16 16">
        <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
        <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4"/>
        </svg></div>`
    }
    singleDisplay.innerHTML = tempHTML
    for (const property in related) {
        let currentProperty = related[property]
        for (const i in currentProperty) {
            let currentItem = currentProperty[i]
            for (const j in currentItem) {
                if (j.includes('id')) {
                    continue
                }
                let tempButton = document.getElementById(`${property}-${j}`)
                // console.log(tempButton)
                tempButton.onclick = event => {
                    let tempEndpoint = relationMap[currentOpen['table_endpoint']][property]
                    let noNames = tempEndpoint.replace('-names', '')
                    sendSignal(noNames)
                }
            }
        }
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
        let tempTarget = 0
        for (let i = 0;i<openTableRows.length;i++) {
            if (openTableRows[i].id == idNum) {
                tempTarget = i
            }
        }
        // console.log("TEMP TARGET: " + tempTarget)
        popupBuilderArbiter(currentOpen['table'], tempTarget)
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
    sendSignal('/actor')
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

function inputBoxBuilderNum(dataNameStr, initialValue) {
    let htmlString = `<label for="${dataNameStr}">${formatNormal(dataNameStr)}</label>`
    htmlString += `<input type="number" id="${dataNameStr}-input" placeholder='${dataNameStr}' value='${initialValue}'/>`
    return htmlString
}
async function queryConnectiveAndEndcap(value) {}


async function foreignDataQuerier(currentRequested, itemNum) {
    let htmlWork = ``
    for (const value of currentRequested['foreign_keyed']) {
        let actualValue = Object.entries(value)[0]
        if (value.value == 'id') {
            continue
        }
        if (!actualValue[0].includes('_id')) {
            console.log('wabba')
            let returnedData = await getConnectiveData(actualValue[0]).then(data => {return data})
            htmlWork += dropdownBuilder('', returnedData.data, actualValue[0])
        } else if (actualValue[0] != currentOpen['table_endpoint'].slice(1) + '_id') {
            let returnedData = await getEndcapData(actualValue[0]).then(data => {return data})
            htmlWork += dropdownBuilder('', returnedData, actualValue[0], itemNum)
        }
    }
    return htmlWork
}


async function popupBuilderArbiter(tableSelected, itemNum) {
    // console.log('ITEM NUM' + itemNum)
    tableSelected = tableSelected.replace('-', '_')
    let popUpWindow = document.getElementById('popup')
    let currentRequested = tableData[tableSelected]
    // console.log('INDEX: ' + currentOpen['item'])
    // console.log("HUH :" + openTableRows[currentOpen['item']].id)
    // console.log(tableSelected)
    // console.log(currentRequested)
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
        for (const key of currentRequested['non_foreign']) { //refactor to make it build number input boxes
            // console.log(key)
            listKeys.push(key)
        }
        listKeys = sortIt(orderDataDict[tableSelected], listKeys)
        // console.log(listKeys)
        for (const key in listKeys) {
            if (key.includes('_id')) {
                continue
            }
            // console.log(key)
            if (listKeys[key] == 'INTEGER' || listKeys[key] == "FLOAT") {
                if (itemNum == null) {
                    htmlString += inputBoxBuilderNum(key, 0)
                    continue
                } else {
                    htmlString += inputBoxBuilderNum(key, openTableRows[itemNum][key]) // LOOK UP What num is supposed to be
                    continue
                }
            }
            if (itemNum == null) {
                htmlString += inputBoxBuilder(key, key)
                continue
            } else {
                htmlString += inputBoxBuilder(key, openTableRows[itemNum][key])
                continue
            }
        }
    } catch (error) {
        console.log(error)
    }
    try {
        htmlString += await foreignDataQuerier(currentRequested, itemNum)
    } catch (error) {
        console.log(error)
    }


    htmlString += `<input type='submit' id='popup-submit' value='Submit' id='popup-submit'></form></div></div></div>`
    popUpWindow.innerHTML = htmlString
    if (itemNum != null) {
        for (const value of currentRequested['foreign_keyed']) {
            let actualValue = Object.entries(value)[0]
            if(actualValue[0] == 'id') {
                continue
            }
            let tempSelection = document.getElementById('selection-' + actualValue[0])
            tempSelection.selectedIndex = parseInt(openTableRows[itemNum][actualValue[0]]) - 1
        }
    }
    let popupBackground = document.getElementById('popupbkg')
    popupBackground.onclick = ev => {
        closeAddingWindow()
    }
    let form = document.getElementById('popup-right')
    let formData = {}
    form.addEventListener('submit', event => {
        event.preventDefault()
        //loop through and get values of all strings
        formData['id'] = currentOpen['item']
        for (const value of currentRequested['non_foreign']) {
            let actualValue = Object.entries(value)[0][0]
            // console.log(actualValue)
            if (actualValue.includes('_id') || actualValue == 'id'){
                continue
            }
            formData[actualValue] = document.getElementById(actualValue + '-input').value
        }
        for (const value of currentRequested['foreign_keyed']) {
            let actualValue = Object.entries(value)[0][0]
            if (actualValue == currentOpen['table_endpoint'].slice(1) + '_id') {
                console.log('key found')
                formData[actualValue] = currentOpen['item']
                continue
            }
            // console.log(key)
            formData[actualValue] = parseInt(document.getElementById('selection-' + actualValue).value)
        }
        const loreconn = "/";
        // console.log(formData)
        let targetEndpoint = tableSelected.replace('_table', '').replace(/_/g, '-')
        // console.log(targetEndpoint)
        if (itemNum == null) {
            axios.post(loreconn + targetEndpoint, data=formData)
            .then(response => {
            console.log(response)
            })
            .catch(error => {
                console.log(error)
            });
        } else {
            formData['id'] = currentOpen['item']
            axios.put(loreconn + targetEndpoint, data=formData)
            .then(response => {
                console.log(response)
            })
            .catch(error => {
                console.log(error)
            })
        }
        sendSignal(currentOpen['table_endpoint'])
            closeAddingWindow()
        })
    return htmlString
}

function addButtonTopFunction() {
    popupBuilderArbiter(currentOpen['table'], null)
}

function sortIt(orderedExampleList, toSortList) {

    result = {}

    tempDict = {}

    for (let i = 0;i<toSortList.length;i++) {
        tempList = Object.entries(toSortList[i])
        tempDict[tempList[0][0]] = tempList[0][1]
        // console.log(tempList)
    }

    for (let i =0;i<orderedExampleList.length;i++) {
        result[orderedExampleList[i]] = tempDict[orderedExampleList[i]]
    }

    return result
}

// function sortItToList(orderedExampleList, toSortList) {
//     result = []

//     for (let i = 0;i<orderedExampleList.length;i++) {
//         result += {
//             orderedExampleList[i]: toSortList[orderedExampleList[i]]
//         }
//     }
//     return result
// }

function listToDict(list) {
    result = {}
    for (let i = 0;i<list.length;i++) {
        result[list[i][0]] = list[i][1]
    }
    return result
}

function sortDictToList(orderedExampleList, toSortDict) {
    result = []
    for (let i = 0;i<orderedExampleList.length;i++) {
        result.push([orderedExampleList[i], toSortDict[orderedExampleList[i]]])
    }
    return result
}

loadOrderData()
loadTables()


