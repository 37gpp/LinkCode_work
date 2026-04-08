/**
 * @param {string} s
 * @return {number}
 */

var lengthOfLongestSubstring = function (s) {
  let maxLength = 0;

  for (let i = 0; i < s.length; i++) {
    let sub = ""; // reset substring for each start

    for (let j = i; j < s.length; j++) {
      // if character already exists -> stop this substring
      if (sub.includes(s[j])) {
        break;
      }

      // add character to substring
      sub = sub + s[j];

      // update maxLength
      if (sub.length > maxLength) {
        maxLength = sub.length;
      }
    }
  }

  return maxLength;
};

console.log(lengthOfLongestSubstring("abcabcbb"));
