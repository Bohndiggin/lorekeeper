const connection = "http://127.0.0.1:8000";

// let displayArea = document.getElementById('object-display')
// let singleDisplay = document.getElementById('single-display')

Hooks.on("renderSidebarTab", async (app, html) => {
    if (app instanceof JournalDirectory) {
      let button = $("<button class='dmdms'>DMDMS</button>")
  
      button.click(function () {
        new DMDMS().render(true);
      });
  
      html.find(".directory-footer").append(button);
    }
  })
  
  Hooks.on("init", () => {
    game.settings.register("dmdms", "settings", {
      name: "Server Location",
      scope: "world",
      config: false,
      default: {
        server: 'http://127.0.0.1:8000'
      }
    })
  })
  
  
  
  
  class DMDMS extends FormApplication {
  
  
    static get defaultOptions() {
      const options = super.defaultOptions;
      options.id = "dmdms";
      options.template = "modules/dmdms/index.html"
      options.classes.push("dmdms");
      options.resizable = false;
      options.height = "auto";
      options.width = 400;
      options.minimizable = true;
      options.title = "Dungeon Master Data Managment System"
      return options;
    }

    activateListeners(html) {
        super.activateListeners(html)
        html.find('#actor-btn').onclick = async ev => sendSignal('/actor', html);
        html.find('#faction-btn').onclick = async ev => sendSignal('/faction', html);
        html.find('#location-btn').onclick = async ev => sendSignal('/location', html);
        html.find('#historical-fragments-btn').onclick = async ev => sendSignal('/historical-fragments', html);
        html.find('#object-btn').onclick = async ev => sendSignal('/object', html);
        html.find('#world-data-btn').onclick = async ev => sendSignal('/world-data', html);
    }
  }
  


function writeTable(response, endpoint, html){
    let display = html.getElementById('object-display')
    display.innerHTML = ""
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
        display.innerHTML += tableHTML
        // console.log(`${values[0]}-${values[1]}`)
        // document.getElementById(`${values[0]}-${values[1]}`).onclick = () => console.log(`${endpoint}/?id=${values[0]}`)
    }
    tableHTML += `</table>`
    display.innerHTML = tableHTML
    for (let i = 0;i<response.data.length;i++){
        let values = Object.values(response.data[i])
        document.getElementById(`${values[0]}-${values[1]}`).onclick = () => sendOneSignal(`${endpoint}/?id=${values[0]}`)
    }
}

function writeOne(data, html) {
    let singleDisplay = html.getElementById('single-display')
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

function sendSignal(endpoint, html) {
    axios.get(connection + endpoint)
        .then((response) => writeTable(response, endpoint, html))
        .catch((error) => console.log(error))
}

document.getElementById('actor-btn').onclick = () => sendSignal('/actor');
document.getElementById('faction-btn').onclick = () => sendSignal('/faction');
document.getElementById('location-btn').onclick = () => sendSignal('/location');
document.getElementById('historical-fragments-btn').onclick = () => sendSignal('/historical-fragments');
document.getElementById('object-btn').onclick = () => sendSignal('/object');
document.getElementById('world-data-btn').onclick = () => sendSignal('/world-data');
