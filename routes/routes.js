const express = require("express");
const getLaptop = require("../controllers/laptopController");

const router = express.Router();

router.get("/laptops", getLaptop);

module.exports = {
  routes: router,
};
