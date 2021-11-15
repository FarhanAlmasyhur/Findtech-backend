import express, { json, urlencoded } from "express";
import cors from "cors";
import { port, url } from "./config.js";
import routes from "./server/routes/routes.js";

const app = express();

app.use(json());
app.use(cors());
app.use(urlencoded());

app.use("/api", routes);

app.listen(port, () => console.log("App is listening on url " + url));
