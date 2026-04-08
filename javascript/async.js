// function task1(callback) {
//   setTimeout(() => {
//     console.log("Task 1 completed");
//     callback();
//   }, 1000);
// }

// function task2() {
//   console.log("Task 2 completed");
// }

// task1(task2);

// function task1() {
//   setTimeout(() => {
//     console.log("Task 1: Data fetched from server");
//   }, 1000);
// }

// function task2() {
//   console.log("Task 2: Printing the data...");
// }

// task1();
// task2();

function task1(callback) {
  setTimeout(() => {
    console.log("Task 1: Data fetched from server");

    // 2. Call the function here, AFTER the data is "fetched"
    callback();
  }, 1000);
}

function task2() {
  console.log("Task 2: Printing the data...");
}

// 3. Pass task2 as an argument (don't use parentheses here!)
task1(task2);
