// const fs = require("fs");
// function fileOperation() {
//   //write

//   fs.writeFile("file.txt", "This is a file created using Node.js", (err) => {
//     console.log("writting to the file has happened successfully !!!");
//   });
// }
// module.exports = fileOperation;
//non blocking io

// async function fileOperation() {
//   try {
//     await fs.appendFile("file.txt", "\nThis is a new updated data!!!0");
//     console.log("file is updated");
//   } catch (err) {
//     console.error("error in updating a file:", err);
//   }
//   fs.readFile("file.txt", "utf-8", (err, data) => {
//     if (err) {
//       console.log("errorrrrrrrrr");
//     }
//     console.log(data);
//   });

//updating the content of the file
// }
// module.exports = fileOperation;

//non blocking sathi readFileSyn  // gives data in buffer format  so need to convert it toString() ani writeFileSyn use karayche
//update and delete operations
//react for frontend and node for backend  for both we need js only
//node js to run js apart from browser
//node js is used to build server side application .
// both uses npm node package manager to install packages and dependencies

const fs = require("fs").promises;

async function fileOperation() {
  try {
    await fs.appendFile("file.txt", "\nThis is my new data!!");
    console.log("file updated");
  } catch (err) {
    console.error("This is an error:", err);
  }
}

module.exports = fileOperation;


