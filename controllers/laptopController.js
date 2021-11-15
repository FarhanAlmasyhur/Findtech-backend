const firebase = require("../db");
const Laptop = require("../models/laptop");

const getLaptop = async (req, res) => {
  try {
  } catch (error) {
    res.status(400).send(error.message);
  }
};

module.exports = getLaptop;
