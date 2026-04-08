//for loop
let n = 5;
let sum = 0;
for (let i = 0; i < n; i++) {
  sum += i + 1;
}
console.log(sum);
//sum of natural numbers
let c = 1 + 2 + 3 + 4 + 5;
console.log(c);

//for-in loop
let obj = {
  shreya: 94,
  gayatri: 88,
  diksha: 94,
  sapna: 92,
};

for (let b in obj) {
  console.log("Marks of " + a + " are " + obj[b]);
}

// OUTPUT
// VM87:9 Marks of [object SVGClipPathElement] are 94
// VM87:9 Marks of [object SVGClipPathElement] are 88
// VM87:9 Marks of [object SVGClipPathElement] are 94
// VM87:9 Marks of [object SVGClipPathElement] are 92
// undefined

//for of loop
for (let b in "DIKSHA") {
  console.log(b);
}
