/**
 * @param {string} s
 * @return {number}
 */

let s = "LI";
var romanToInt = function (s) {
  let map = {
    I: 1,
    V: 5,
    X: 10,
    L: 50,
    C: 100,
    D: 500,
    M: 1000,
  };

  let result = 0;

  let integer = s.split("").map(function (elem) {
    return map[elem];
  });

  for (let i = 0; i < integer.length; i++) {
    if (integer[i] < integer[i + 1]) {
      result += integer[i + 1] - integer[i];
      i++;
    } else {
      result += integer[i];
    }
  }

  return result;
};
console.log(romanToInt(s));
