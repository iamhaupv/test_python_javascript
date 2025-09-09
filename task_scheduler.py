from collections import OrderedDict

class TaskScheduler:
    def __init__(self):
        # Dùng OrderedDict để giữ thứ tự thêm task
        self._tasks = OrderedDict()
        self._results = {}

    def add_task(self, name: str, func: callable):
        """Thêm tác vụ mới. Nếu tên đã tồn tại -> raise ValueError."""
        if name in self._tasks:
            raise ValueError(f"Task '{name}' already exists")
        if not callable(func):
            raise TypeError("Task function must be callable")
        self._tasks[name] = func

    def remove_task(self, name: str):
        """Xóa tác vụ. Nếu không tồn tại -> raise KeyError."""
        if name not in self._tasks:
            raise KeyError(f"Task '{name}' not found")
        del self._tasks[name]
        if name in self._results:
            del self._results[name]

    def run_all(self):
        """Chạy tất cả task theo thứ tự thêm vào, lưu kết quả hoặc exception message."""
        self._results.clear()
        for name, func in self._tasks.items():
            try:
                self._results[name] = func()
            except Exception as e:
                self._results[name] = f"{type(e).__name__}: {e}"

    def get_results(self) -> dict[str, object]:
        """Trả về dict {task_name: result}."""
        return dict(self._results)
import unittest

class TestTaskScheduler(unittest.TestCase):
    def setUp(self):
        self.scheduler = TaskScheduler()

    # --- Trường hợp cơ bản ---
    def test_add_and_run_tasks(self):
        def f1(): return 1
        def f2(): return "hello"
        self.scheduler.add_task("t1", f1)
        self.scheduler.add_task("t2", f2)
        self.scheduler.run_all()
        results = self.scheduler.get_results()
        self.assertEqual(results["t1"], 1)
        self.assertEqual(results["t2"], "hello")

    # --- Thêm trùng tên ---
    def test_add_duplicate_task(self):
        def f(): return 1
        self.scheduler.add_task("t1", f)
        with self.assertRaises(ValueError):
            self.scheduler.add_task("t1", f)

    # --- Xóa task ---
    def test_remove_task(self):
        def f(): return 42
        self.scheduler.add_task("t1", f)
        self.scheduler.remove_task("t1")
        with self.assertRaises(KeyError):
            self.scheduler.remove_task("t1")

    # --- Hàm không callable ---
    def test_add_non_callable(self):
        with self.assertRaises(TypeError):
            self.scheduler.add_task("t1", 123)

    # --- Task bị lỗi ---
    def test_task_with_exception(self):
        def f(): raise RuntimeError("fail")
        self.scheduler.add_task("t1", f)
        self.scheduler.run_all()
        results = self.scheduler.get_results()
        self.assertIn("RuntimeError: fail", results["t1"])

    # --- Chạy nhiều lần ---
    def test_run_multiple_times(self):
        def f1(): return "first"
        def f2(): return "second"
        self.scheduler.add_task("t1", f1)
        self.scheduler.add_task("t2", f2)

        self.scheduler.run_all()
        r1 = self.scheduler.get_results()
        self.assertEqual(r1["t1"], "first")

        # thay đổi hàm rồi chạy lại
        self.scheduler.remove_task("t1")
        def f1b(): return "first_modified"
        self.scheduler.add_task("t1", f1b)

        self.scheduler.run_all()
        r2 = self.scheduler.get_results()
        self.assertEqual(r2["t1"], "first_modified")

    # --- Không có task nào ---
    def test_no_tasks(self):
        self.scheduler.run_all()
        self.assertEqual(self.scheduler.get_results(), {})

    # --- Task có side effect ---
    def test_task_with_side_effect(self):
        data = []
        def f(): 
            data.append(1)
            return sum(data)
        self.scheduler.add_task("t1", f)
        self.scheduler.add_task("t2", f)
        self.scheduler.run_all()
        results = self.scheduler.get_results()
        self.assertEqual(results["t1"], 1)
        self.assertEqual(results["t2"], 2)

    # --- Exception khác nhau ---
    def test_different_exceptions(self):
        def f1(): raise ValueError("bad")
        def f2(): raise ZeroDivisionError("div0")
        self.scheduler.add_task("t1", f1)
        self.scheduler.add_task("t2", f2)
        self.scheduler.run_all()
        results = self.scheduler.get_results()
        self.assertEqual(results["t1"], "ValueError: bad")
        self.assertEqual(results["t2"], "ZeroDivisionError: div0")


if __name__ == "__main__":
    unittest.main()
