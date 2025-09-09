function topKFrequent(nums, k) {
  const freqMap = new Map();

  for (let num of nums) {
    freqMap.set(num, (freqMap.get(num) || 0) + 1);
  }

  const sorted = [...freqMap.entries()].sort((a, b) => b[1] - a[1]);
  return sorted.slice(0, k).map(entry => entry[0]);
}
console.log(topKFrequent([1,1,1,2,2,3], 2)); // [1,2]
console.log(topKFrequent([4,4,4,4,5,5,6], 1)); // [4]
console.log(topKFrequent([1], 1)); // [1]
console.log(topKFrequent([1,2,3,4,5], 3)); // có thể [1,2,3] (vì tần suất đều 1)

