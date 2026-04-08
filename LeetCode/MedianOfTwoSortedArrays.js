let nums1 = [1, 2];
let nums2 = [3, 4];
var findMedianSortedArrays = function (nums1, nums2) {
  let nums = nums1.concat(nums2).sort((a, b) => a - b); // combine arrays
  let n3 = nums.length;
  n3 = Math.floor(n3);

  if (n3 % 2 == 0) {
    var mid = n3 / 2;

    let a = mid - 1;
    let b = mid;

    let median = (nums[a] + nums[b]) / 2;
    return median;
  } else {
    let medianindex = Math.floor(n3 / 2);
    let median = nums[medianindex];
    return median;
  }
};
console.log(findMedianSortedArrays(nums1, nums2));
//EXPECTED SOLUTION \|/
//                     var findMedianSortedArrays = function(nums1, nums2) {

//     if (nums1.length > nums2.length) {
//         [nums1, nums2] = [nums2, nums1];
//     }

//     let x = nums1.length;
//     let y = nums2.length;

//     let low = 0;
//     let high = x;

//     while (low <= high) {

//         let partitionX = Math.floor((low + high) / 2);
//         let partitionY = Math.floor((x + y + 1) / 2) - partitionX;

//         let maxLeftX = partitionX == 0 ? -Infinity : nums1[partitionX - 1];
//         let minRightX = partitionX == x ? Infinity : nums1[partitionX];

//         let maxLeftY = partitionY == 0 ? -Infinity : nums2[partitionY - 1];
//         let minRightY = partitionY == y ? Infinity : nums2[partitionY];

//         if (maxLeftX <= minRightY && maxLeftY <= minRightX) {

//             if ((x + y) % 2 == 0) {
//                 return (Math.max(maxLeftX, maxLeftY) + Math.min(minRightX, minRightY)) / 2;
//             } else {
//                 return Math.max(maxLeftX, maxLeftY);
//             }

//         } 
//         else if (maxLeftX > minRightY) {
//             high = partitionX - 1;
//         } 
//         else {
//             low = partitionX + 1;
//         }
//     }
// };