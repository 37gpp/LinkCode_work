function add() {
  alert("Enter two numbers to add");
  let x = parseInt(prompt("Number one:"));
  let y = parseInt(prompt("Number two:"));

  let sum = x + y;
  // alert(sum);
  // return sum;
  document.getElementById("Answer").innerHTML = x + y;
}
function sub() {
  alert("Enter two numbers to substract");
  let x = parseInt(prompt("Number one:"));
  let y = parseInt(prompt("Number two:"));
  let sum = x - y;
  return sum;
}
function mul() {
  alert("Enter two numbers to Multiply");
  let x = parseInt(prompt("Number one:"));
  let y = parseInt(prompt("Number two:"));
  let sum = x * y;
  return sum;
}
function div() {
  alert("Enter two numbers to Divide");
  let x = parseInt(prompt("Number one:"));
  let y = parseInt(prompt("Number two:"));
  let sum = x / y;
  return sum;
}
