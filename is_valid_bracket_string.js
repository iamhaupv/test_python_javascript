function isValidBracketString(s) {
  const stack = [];
  const pairs = {
    ")": "(",
    "]": "[",
    "}": "{"
  };

  for (let ch of s) {
    if (["(", "[", "{"].includes(ch)) {
      stack.push(ch); // gặp ngoặc mở thì push vào stack
    } else if ([")", "]", "}"].includes(ch)) {
      if (stack.length === 0 || stack.pop() !== pairs[ch]) {
        return false; // không khớp hoặc stack rỗng
      }
    } else {
      // Nếu xuất hiện ký tự không hợp lệ
      return false;
    }
  }

  return stack.length === 0; // cuối cùng stack phải rỗng
}
console.log(isValidBracketString("()[]{}"));   // true
console.log(isValidBracketString("([{}])"));   // true
console.log(isValidBracketString("(]"));       // false
console.log(isValidBracketString("([)]"));     // false
console.log(isValidBracketString("((("));      // false
console.log(isValidBracketString(""));         // true
