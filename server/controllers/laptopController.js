import { ref, onValue } from "firebase/database";
import db from "../../db.js";
import Laptop from "../models/laptop.js";

const laptopRef = ref(db, "/Laptops");

const getLaptop = async (req, res) => {
  const laptopArray = [];
  try {
    onValue(laptopRef, (snapshot) => {
      snapshot.forEach((items) => {
        const laptopValue = items.val();
        const laptop = new Laptop(
          items.key,
          laptopValue.Name,
          laptopValue.Price,
          laptopValue.Image
        );
        laptopArray.push(laptop);
      });
      res.status(200).send(laptopArray);
    });
  } catch (err) {
    console.log(err);
    res.status(400).send(err.message);
  }
};

export default getLaptop;
