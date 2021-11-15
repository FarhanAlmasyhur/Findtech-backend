import { Router } from "express";
import getLaptop from "../controllers/laptopController.js";

const router = Router();

router.get("/laptops", getLaptop);

const routes = router;

export default routes;
