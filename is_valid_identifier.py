import re
import keyword
import unittest

def is_valid_identifier(s: str) -> bool:
    """
    Kiểm tra xem chuỗi s có phải là tên biến hợp lệ trong Python không.
    Quy tắc:
      - Chỉ chứa chữ cái (A-Z, a-z), chữ số (0-9) hoặc dấu gạch dưới (_)
      - Không bắt đầu bằng số
      - Không trùng với từ khóa của Python
    """
    if not isinstance(s, str):
        return False
    if s == "":
        return False
    if keyword.iskeyword(s):
        return False
    return bool(re.match(r'^[A-Za-z_][A-Za-z0-9_]*\Z', s))


# ================== UNIT TESTS ==================
class TestIsValidIdentifier(unittest.TestCase):
    # --- Trường hợp hợp lệ ---
    def test_valid_simple(self):
        self.assertTrue(is_valid_identifier("abc"))
        self.assertTrue(is_valid_identifier("x"))
        self.assertTrue(is_valid_identifier("_"))
        self.assertTrue(is_valid_identifier("_var"))
        self.assertTrue(is_valid_identifier("var123"))
        self.assertTrue(is_valid_identifier("snake_case"))
        self.assertTrue(is_valid_identifier("UPPERCASE"))
        self.assertTrue(is_valid_identifier("Mix_Case123"))
        self.assertTrue(is_valid_identifier("_"*50))  # toàn dấu gạch dưới
        self.assertTrue(is_valid_identifier("longname_" + "a"*100))  # rất dài

    # --- Sai: bắt đầu bằng số ---
    def test_invalid_start_digit(self):
        self.assertFalse(is_valid_identifier("1var"))
        self.assertFalse(is_valid_identifier("123"))
        self.assertFalse(is_valid_identifier("9_x"))
        self.assertFalse(is_valid_identifier("0abc"))

    # --- Sai: chứa ký tự đặc biệt ---
    def test_invalid_special_chars(self):
        invalids = ["a-b", "a b", "a.b", "name$", "test!", "hello@", "good#name",
                    "percent%", "comma,", "semi;", "colon:", "slash/", "back\\slash"]
        for s in invalids:
            with self.subTest(s=s):
                self.assertFalse(is_valid_identifier(s))

    # --- Sai: khoảng trắng ---
    def test_invalid_with_whitespace(self):
        self.assertFalse(is_valid_identifier(" abc"))
        self.assertFalse(is_valid_identifier("abc "))
        self.assertFalse(is_valid_identifier("a b c"))
        self.assertFalse(is_valid_identifier("\tabc"))
        self.assertFalse(is_valid_identifier("new\nline"))

    # --- Sai: chuỗi rỗng ---
    def test_empty_string(self):
        self.assertFalse(is_valid_identifier(""))

    # --- Sai: trùng từ khóa ---
    def test_keywords(self):
        for kw in keyword.kwlist:
            with self.subTest(kw=kw):
                self.assertFalse(is_valid_identifier(kw))

    # --- Unicode / Non-ASCII ---
    def test_non_ascii(self):
        self.assertFalse(is_valid_identifier("éclair"))   # é
        self.assertFalse(is_valid_identifier("naïve"))    # ï
        self.assertFalse(is_valid_identifier("变量"))     # tiếng Trung
        self.assertFalse(is_valid_identifier("привет"))   # Cyrillic
        self.assertFalse(is_valid_identifier("name\u200b"))  # zero-width space

    # --- Input không phải chuỗi ---
    def test_non_string_inputs(self):
        self.assertFalse(is_valid_identifier(None))
        self.assertFalse(is_valid_identifier(123))
        self.assertFalse(is_valid_identifier(12.3))
        self.assertFalse(is_valid_identifier(["abc"]))
        self.assertFalse(is_valid_identifier(b"abc"))

    # --- Edge cases ---
    def test_edge_cases(self):
        self.assertTrue(is_valid_identifier("a"*1000))  # rất dài
        self.assertTrue(is_valid_identifier("_a"*500))  # pattern dài
        # async/await (keyword trong Python 3.7+)
        if keyword.iskeyword("async"):
            self.assertFalse(is_valid_identifier("async"))
        else:
            self.assertTrue(is_valid_identifier("async"))
        if keyword.iskeyword("await"):
            self.assertFalse(is_valid_identifier("await"))
        else:
            self.assertTrue(is_valid_identifier("await"))

    # --- Ví dụ trong đề ---
    def test_examples_from_prompt(self):
        self.assertTrue(is_valid_identifier("abc"))
        self.assertFalse(is_valid_identifier("123var"))
        self.assertFalse(is_valid_identifier("for"))


if __name__ == "__main__":
    unittest.main()
