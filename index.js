const express = require("express");
const cors = require("cors");
const config = require("./config");
const routes = require("./routes/routes");

const app = express();

app.use(express.json());
app.use(cors());
app.use(express.urlencoded());

app.use("/api", routes.routes);

app.listen(config.port, () =>
  console.log("App is listening on url " + config.host)
);
