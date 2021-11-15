const firebase = require("firebase");
const config = require("./config");

firebase.initializeApp(config.firebaseConfig);

let db = firebase.database();

module.exports = db;
