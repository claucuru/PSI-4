const { defineConfig } = require("cypress");

module.exports = defineConfig({
  e2e: {
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
    defaultCommandTimeout: 10000, // 10 seconds
    // append baseUrl to all URL used in the tests
    baseUrl: "http://localhost:5173",
    //specPattern: "cypress/e2e/**/*.{js,jsx,ts,tsx}",
  },
  // centralice some variables as username and password
  // use then in the test with "Cypress.env('username')"
  env: {
    username: "y",
    password: "y",
    // python: "/home/roberto/miniconda/envs/chess/bin/python",
    //python: "/mnt/c/Users/Usuario/OneDrive\\ -\\ UAM/Documentos/GitHub/PSI-4/p4_env/bin/python3",
    python: "/home/alejandra-palma/Documentos/GitHub/PSI-4/venv/bin/python",
    //python: "~/PSI-4/p4_env/bin/python",
    //manage: "~/PSI-4/chesstournament/manage.py",
    //manage: "/home/roberto/Docencia/psi/2024-25/chesstournament/chesstournament_server/manage.py",
    //manage: "/mnt/c/Users/Usuario/OneDrive\\ -\\ UAM/Documentos/GitHub/PSI-4/chesstournament/manage.py",
    manage: "/home/alejandra-palma/Documentos/GitHub/PSI-4/chesstournament/manage.py",
  },
});
