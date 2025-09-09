from collections import defaultdict
import unittest

def group_anagrams(words: list[str]) -> list[list[str]]:
    """
    Nhóm các từ anagram lại với nhau.
    - Hai từ là anagram nếu khi sắp xếp ký tự chúng giống nhau.
    - Trả về danh sách các nhóm (thứ tự nhóm/ phần tử trong nhóm không quan trọng).
    """
    groups = defaultdict(list)
    for word in words:
        # key là tuple ký tự đã sắp xếp
        key = tuple(sorted(word))
        groups[key].append(word)
    return list(groups.values())
class TestGroupAnagrams(unittest.TestCase):
    # --- Trường hợp cơ bản ---
    def test_example_case(self):
        words = ["eat", "tea", "tan", "ate", "nat", "bat"]
        result = group_anagrams(words)
        expected_groups = [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
        # Chuyển về set để so sánh không phụ thuộc thứ tự
        self.assertEqual({frozenset(g) for g in result}, {frozenset(g) for g in expected_groups})

    # --- Chuỗi rỗng ---
    def test_empty_input(self):
        self.assertEqual(group_anagrams([]), [])

    def test_single_empty_string(self):
        self.assertEqual(group_anagrams([""]), [[""]])

    def test_multiple_empty_strings(self):
        result = group_anagrams(["", "", ""])
        self.assertEqual(result, [["", "", ""]])  # tất cả empty vào 1 nhóm

    # --- Một phần tử ---
    def test_single_word(self):
        self.assertEqual(group_anagrams(["abc"]), [["abc"]])

    # --- Không có anagram ---
    def test_no_anagrams(self):
        words = ["abc", "def", "ghi"]
        result = group_anagrams(words)
        expected = [["abc"], ["def"], ["ghi"]]
        self.assertEqual({frozenset(g) for g in result}, {frozenset(g) for g in expected})

    # --- Tất cả là anagram của nhau ---
    def test_all_anagrams(self):
        words = ["abc", "cab", "bca", "cba"]
        result = group_anagrams(words)
        self.assertEqual(len(result), 1)
        self.assertEqual(set(result[0]), {"abc", "cab", "bca", "cba"})

    # --- Phân biệt hoa thường ---
    def test_case_sensitive(self):
        words = ["abc", "Abc", "CAB"]
        result = group_anagrams(words)
        # "abc" khác "Abc" vì Python sort phân biệt hoa thường
        expected = [["abc"], ["Abc"], ["CAB"]]
        self.assertEqual({frozenset(g) for g in result}, {frozenset(g) for g in expected})

    # --- Có ký tự đặc biệt ---
    def test_with_special_characters(self):
        words = ["a!b", "b!a", "!ab", "xyz"]
        result = group_anagrams(words)
        expected = [["a!b", "b!a", "!ab"], ["xyz"]]
        self.assertEqual({frozenset(g) for g in result}, {frozenset(g) for g in expected})

    # --- Từ dài ---
    def test_long_words(self):
        words = ["a"*100, "a"*99 + "b", "b" + "a"*99]
        result = group_anagrams(words)
        self.assertEqual(len(result), 2)
        groups = {frozenset(g) for g in result}
        self.assertIn(frozenset(["a"*100]), groups)
        self.assertIn(frozenset(["a"*99 + "b", "b" + "a"*99]), groups)


if __name__ == "__main__":
    unittest.main()
