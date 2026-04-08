const mongoose = require("mongoose");
//note model . js needs the mongoose package to be installed again

//creating the mongoose schema
const noteSchema = new mongoose.Schema({
  title: String,
  description: String,
});

const noteMOdel = mongoose.model("note", noteSchema);
//noteModel . see we have created the schema to tell the db what type of data we are going to save in it . now we create model to create the collection in db
// i mean model is used to perform CRUD operations on the collection
//now we will export the model to use it in other files
module.exports = noteMOdel;

//model folder is created to store the models the models are the blueprints of the collection in the database