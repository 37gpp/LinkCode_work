
//function
function onePlusAverage(x, y) {
  return 1 + (x + y) / 2;
}

let a = 1;
let b = 2;
let c = 3;

let Ans = onePlusAverage(a, b);
console.log(Ans);

let Anss = onePlusAverage(c, b);
console.log(Anss);

//Another way to write function
const sum = (x, y, z) => {
  return x + y + z;
};

let d = sum(a, b, c);
console.log(d);

//one more
const hello = () => {
  console.log("Hey how are you. I am toh fine yaar");
};
hello();

//write a program to print the marks of a student in an object using the for loop
const obj = {
  harry: 98,
  rohan: 70,
  akash: 7,
};

for (let a in obj) {
  console.log("Marks of " + a + " " + "is " + obj[a]);
}

for (let i = 0; i < Object.keys(obj).length; i++) {
  console.log(
    "The marks of " +
      Object.keys(obj)[i] +
      "is" +
      " " +
      obj[Object.keys(obj)[i]]
  );
}

//write a program to print "try again" until the users enters the correct number.
let correctNum = 44;
let i;
// while (i != correctNum) {
//   i = prompt("Enter a number");
// console.log("Try again");
// }

// console.log("You have entered a correct number");//Run it in a console.
