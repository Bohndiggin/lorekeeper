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
  }
  


