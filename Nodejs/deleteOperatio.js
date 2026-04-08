const fs = require("fs").promises;

async function deleteOperation() {
  try {
    let data = await fs.readFile("file.txt", "utf-8");

    let updateData = data.replace("This is a file created", " ");

    fs.writeFile("file.txt", updateData);
    console.log("file content is deleted");
  } catch (err) {
    console.error(err);
  }
}

module.exports = deleteOperation;
//npm init
//npm i nodemon
//common js / Es6 modules
//module.exports
//for impoting we use require() in common js and import in es6 modules
//named exports in node we use {} for named exports and in es6 we use export
//  const name = value; and for default export we use export default name;
// and in node we use module.exports = name;
//when we import multiple functions using named export we ue dot operator .
//server is a program that listens to the request and send response to the
// client and client is a program that sends request to the server and waits for
// the response from the server.
//to run node on server we need to creae it
//there are two ways to create a server in node js one is using http module and
//  other is using express framework
//to set ort no. u can manually set it or use process.env.PORT to set it dynamically
// and for local development we can use 3000 or 5000 as port no. and for production
// we can use 80 or 443 as port no.
//to create a server using http module we need to require it and then create a server
//  using http.createServer() method and then listen to the port no. using server.listen() method.
//check who returns buffer data then use toString() method to convert it to string data and then
// use it for further operations.
