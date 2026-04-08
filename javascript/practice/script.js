// alert("Enter your age");
// let age = prompt("Enter your age here", "19");
// age = Number.parseInt(age);
// let write = confirm("Do you want write your age on the screen");
// if (write) {
//   document.write(age);
// } else {
//   document.write("allow to write the age please");
// }
// if (age > 18) {
//   alert("you can drive");
// } else {
//   alert("you cannot drive");
// }
// console.log(document.head.firstChild);
// a = document.body.firstChild;
// console.log(a.parentNode);
// console.log(a.parentElement);
// console.log(a.firstChild.nextsibling);

// let b = document.body;
// console.log("first child of b is:", b.firstChild);
// console.log(b.firstElementChild);
// console.error("dont underestimate the power of diksha");
// const changeBgRed = () => {
//   b.firstElementChild.style.backgroundColor = "pink";
// };

// let t = document.body.firstElementChild.firstElementChild;
// console.log(t.rows);
// console.log(t.caption);

// console.log(t.thead);
// console.log(t.tfoot);
// console.log(t.rows[0].rowIndex);
// console.log(TextDecoder.cellIndex);

let t = document.getElementById("fcard-title");
t.style.color = "blue";
let q = document.querySelectorAll(".card-title");
q[0].style.color = "green";
q[1].style.color = "yellow";
q[2].style.color = "blue";

let b = document.querySelectorAll(".btn-primary");
b[0].style.backgroundColor = "yellow";
b[1].style.backgroundColor = "pink";
b[2].style.backgroundColor = "cyan";
