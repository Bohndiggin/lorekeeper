Hooks.on("renderSidebarTab", async (app, html) => {
    if (app instanceof JournalDirectory) {
      let button = $("<button class='dmdms'>DMDMS</button>")
  
      button.click(function () {
        // new DMDMS().render(true);
        let dmdms = new DMDMS()
        dmdms.render(true);
        // objective.activateListeners()
      });
      console.log("yipee")
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
        options.resizable = true;
        options.height = "auto";
        options.width = 400;
        options.minimizable = true;
        options.title = "Dungeon Master Data Managment System"
        return options;
    }
    activateListeners(html) {
        super.activateListeners(html)
        html.ready(console.log('ready'))
        let actorButton = $('#dmdms-actor-btn')
        let factionButton = $('#dmdms-faction-btn')
        let locationButton = $('#dmdms-location-btn')
        let historicalFragmentsButton = $('#dmdms-historical-fragments-btn')
        let objectButton = $('#dmdms-object-btn')
        let worldDataButton = $('#dmdms-world-data-btn')
        actorButton.click((ev) => {this.sendSignal('/actor')});
        factionButton.click(ev => {this.sendSignal('/faction', html)});
        locationButton.click(ev => {this.sendSignal('/location', html)});
        historicalFragmentsButton.click(ev => {this.sendSignal('/historical-fragments', html)});
        objectButton.click(ev => {this.sendSignal('/object', html)});
        worldDataButton.click(ev => {this.sendSignal('/world-data', html)});
        console.log('listening')
    }
    writeTable(response, endpoint){
        let displayArea = $('#object-display')[0]
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
            console.log(`#${values[0]}-${values[1]}`)
            let idClean = values[1].split(' ').join('')
            let buttonTemp = $(`#${values[0]}-${idClean}`)
            console.log(buttonTemp)
            buttonTemp.click(ev => {
                this.sendOneSignal(`${endpoint}/?id=${values[0]}`)
            })
        }
    }
    writeOne(data) {
        let singleDisplay = $('#single-display')[0]
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
    sendOneSignal(endpoint) {
        const dmdmsconn = "http://127.0.0.1:8000";
        console.log(endpoint)
        axios.get(dmdmsconn + endpoint)
            .then((response) => this.writeOne(response.data))
            .catch((error) => console.log(error))
    }
    sendSignal(endpoint) {
        const dmdmsconn = "http://127.0.0.1:8000";
        console.log(endpoint)
        axios.get(dmdmsconn + endpoint)
            .then((response) => this.writeTable(response, endpoint))
            .catch((error) => console.log(error))
    }
}