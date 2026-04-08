let strs = ["slower", "slow", "slight"];

var longestcommonprefix = function (strs) {
  //   if (strs.length === 0) return "";
  //   let temp = strs[0];
  //   for (let i = 1; i < strs.length; i++) {
  //     while (strs[i].indexOf(temp) !== 0) {
  //       //this loop will run until the index of temp words finding in the i th string is not 0
  //       temp = temp.substring(0, temp.length - 1);
  //     }
  //   }
  //   return temp;

  let temp = strs[0];
  for (let i = 0; i < temp.length; i++) {
    for (let j = 1; j < strs.length; j++) {
      if (temp[i] == strs[j][i]) {
        continue;
      } else {
        temp = temp.substring(0, i);
      }
    }
  }
  return temp;
};
console.log(longestcommonprefix(strs));
