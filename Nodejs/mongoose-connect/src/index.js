//create the server
const express = require("express");
const app = express();
const noteModel = require("./models/note-models");

//now we will cretae a note abb where user will be able to post his note
//each note will have the title and description
//before sending data to db we should tell how data will look that is we called schema
//to cretae a schema we create a new folder in src named models
//[4]AApI we are going to create are now post , get , put , delete routes

app.use(express.json());
app.post("/notes", async (req, res) => {
  const data = req.body;
  //now to perform operation we need noteModel
  //crud operations
  //with methods create() , find() , findOne() , findOneAndDelete() , findOneAndUpdate() c=create() , r=read() , u=update() , d=delete() 
  //create method is used to create a new document in the collection like a new note and save it to the database
  await noteModel.create({
    title: data.title,
    description: data.description,
  });
  res.status(201).json({
    message: "Note created successfully",
  });
});

app.get("/notes", async (req, res) => {
  const notes = await noteModel.findOne({
    title: "t1",
  }); //noteModel is used when u are going any work related to the note . it is the collection in db
  //now find() will return an array and that is notes here .
  //we are sending it with response
  //difference between find() and findOne() is that find() returns an array of documents that match the query
  //whereas findOne() returns only the first document that matches the query . it returns object or null
  res.status(200).json({
    message: "Notes fetched successfully",
    notes: notes,
    totalNotes: notes.length,
  });
});

//to delete now we will use the id . u can find it in compass or postman
app.delete("/notes/:id", async (req, res) => {
  const id = req.params.id;
  await noteModel.findOneAndDelete({
    _id: id,
  });
  //we can use deleteOne() , deleteMany() to delete the document that matches the query
  res.status(200).json({
    message: "Note deleted successfully",
  });
});

app.patch("/notes/:id", async (req, res) => {
  const id = req.params.id;
  const description = req.body.description;
  //findOneAndUpdate() is used to update the document that matches the query . it needs to object to be passaed
  await noteModel.findOneAndUpdate(
    {
      _id: id,
    },
    {
      description: description,
    },
  );
  res.status(201).json({
    message: "Note updated successfully",
  });
});
module.exports = app;

//controller folder is used to handle the request and response
//we will create a new file in controller folder named notes-controller.js
//in that file we will write the code to handle the request and response
//we will import this file in index.js
//now suppose instead of directly passing the arrow function in post , get , patch etc if we try to pass controller function there we will do it as
//const handleNotesController = aasync (req, res) => {
//   const data = req.body;
//   await noteModel.create({
//     title: data.title,
//     description: data.description,
//   });
//   res.status(201).json({
//     message: "Note created successfully",
//   });
// };

//frontend features
//update a note page
//home , add new note page
//display notes page
