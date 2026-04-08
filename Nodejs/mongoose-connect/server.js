//server.js is to start the server
const app = require("./src/index");
const connectDB = require("./src/db/db");
const { connect } = require("mongoose");

//we have added this connectDB() in server.js to connect to the database before starting the server
//if we dont add this connectDB() in server.js then the server will start running but the database will not be connected
//so we added this connectDB() in server.js to connect to the database before starting the server

connectDB(); //connectDB function is called to connect to the database

app.listen(3000, () => {
  console.log("Server is running on port 3000");
});
