// const a = require("./node_modules/module");

// const number = 12321;
// console.log(number);
// console.log("Hello, World!");
// const fileOp = require("./fileOperation");
// console.log(" before index.js");
// fileOp();
// console.log(" after index.js");
// blocking madhey fileOp() hya statement sathi lagech swiching to fileOperation file nahin zhala first sagla execute hoil mg last tey hoil

const fileOp = require("./fileOperation");
fileOp();

// const fileOp = require("./deleteOperatio");
// fileOp();

// const http = require("http");
// const fs = require("fs");

// const port = process.env.PORT || 3000;

// const server = http.createServer((req, res) => {
//   res.setHeader("Content-Type", "text/html");
//   if (req.url == "/") {
//     res.statusCode = 200;
//     const data = fs.readFileSync("index.html");
//     res.end(data.toString());
//   } else if (req.url == "/contact.html") {
//     res.statusCode = 200;
//     const data = fs.readFileSync("contact.html");
//     res.end(data.toString());
//   } else if (req.url == "/about.html") {
//     res.statusCode = 200;
//     const data = fs.readFileSync("about.html");
//     res.end(data.toString());
//   } else if (req.url == "/services.html") {
//     res.statusCode = 200;
//     const data = fs.readFileSync("services.html");
//     res.end(data.toString());
//   } else if (req.url == "/portfolio.html") {
//     res.statusCode = 200;
//     const data = fs.readFileSync("portfolio.html");
//     res.end(data.toString());
//   } else {
//     res.statusCode = 404;
//     res.end("<h1>Page Not Found</h1>");
//   }
// });
// server.listen(port, () => {
//   console.log(`server is running on port ${port}`);
// });
//monolithic application madhe sagla code ekach file madhe asel and microservices madhe code alag alag file madhe asel and te ekmekanshi communicate kartil
//clent side rendering madhe server client la data pathavto and client te data process karto and te data user la display karto and server side rendering madhe server client la data pathavto and server te data process karto and te data user la display karto
//=====================================================================
// const express = require("express");
// const mongoose = require("mongoose");

// mongoose
//   .connect(
//     "mongodb+srv://dikshadhanve4_db_user:OynECv2nvryrti9S@cluster1.an6jg4b.mongodb.net/?appName=cluster1",
//   )
//   .then(() => {
//     console.log("database connected successfully");
//   })
//   .catch((err) => {
//     console.error(err);
//   });
// const app = express();
// const port = 3000;

// app.get("/", (req, res) => {
//   res.send("<h1>Welcome to Express Server</h1>");
// });

// app.listen(port, () => {
//   console.log(`serer is listening at port no. ${port}`);
// });

// =====================================================================

//npm i express  to install express framework
//express is a web framework for node js that provides a set of features to develop web and mobile applications. It is a minimal and flexible framework that allows you to create robust APIs and web applications. It provides a simple and intuitive API for routing, middleware, and handling HTTP requests and responses. With express, you can easily create RESTful APIs, serve static files, and handle different HTTP methods like GET, POST, PUT, DELETE, etc. It also has a large ecosystem of middleware and plugins that can be used to extend its functionality.
//put get post delete
//put is used to update the existing data
//  get is used to retrieve the data
// post is used to create new data
//  delete is used to delete the data.
//get is used to retrieve the data from the server and post is used to send the data to the server and put is used to update the existing data on the server and delete is used to delete the data from the server.

//dabase three types mongodb atlas, compass, json .
//    USERNAME: dikshadhanve4_db_user
//dikshadhanve4_db_user
//    PASSWORD: OynECv2nvryrti9S

//mongodb+srv://dikshadhanve4_db_user:OynECv2nvryrti9S@cluster1.an6jg4b.mongodb.net/?appName=cluster1
// theory about express js , node js , react js , angular js , vue js , next js , nest js , svelte js , ember js , backbone js , meteor js , electron js , express js , hapi js , koa js , sails js , loopback js , feathers js , total.js , adonis js , strapi js , keystone js , ghost js , hexo js , gatsby js , nuxt js , gridsome js
// how to use mongo db atlas??


// how to connect the frontend to the backend 
// that to be teached is 26th febrary . 
