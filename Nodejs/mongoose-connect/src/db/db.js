const mongoose = require("mongoose"); //package to connect to mongodb

async function connectDB() {
  await mongoose.connect(
    "mongodb+srv://dikshadhanve4_db_user:wMwDhY7ZDpRm7fBf@mycluster1.mcypxvz.mongodb.net/mydbname",
  ); //connect method connects the database to our local server
  //mydbname is the name of the database we created in mongodb atlas . which comes aftre the .net/. by just giving tis name the new cluster will be created with this name

  console.log("Database connected");
}
//async and await is used because connect method is asynchronous and we want to wait for it to complete before moving on to the next line of code
//actually the server will be connected to db but we are not sure how much time it will take so we used async and await

module.exports = connectDB;
