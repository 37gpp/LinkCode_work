//if else
let a = 5;
let age = 33;
if (age > 18) {
  console.log("you are allowded to drive .");
} else if (age > 0 && age < 18) {
  console.log("you can drive later . please keep patience.");
} else {
  console.log("Enter the valid age");
}

//switch
const exp = "omkar";

switch (exp) {
  case "krish":
    console.log("lambuuu");
    break;
  case "diksha":
    console.log("Topper");
    break;
  default:
    console.log("default");
}

//Converting string to the number
let b = "34";
console.log(typeof b);
b = Number.parseInt(b);
console.log(typeof b);

//ALERT and PROMPT
// alert("This is the alert message ");
// let c = prompt("Enter the age");

//conditional operator
console.log(
  "You can",
  age < 18 ? "Not Drive" : age > 18 ? " Drive" : "Exactly 18"
);

// condition1 ? result1 :
// condition2 ? result2 :
// condition3 ? result3 :
// defaultResult;

//program to find whther the nmber is divisible by 2 and 3

let numb = 6;

if (numb % 2 == 0 && numb % 3 == 0) {
  console.log("Number is divisible by 2 and 3 ");
} else {
  console.log("Number is neither divisible by 2 nor 3");
}
