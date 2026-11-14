import unittest
from ladder import scan, ProgramError

PROGRAM = {"version": 1, "rungs": [{"coil": "run", "expr": {"all": [
    {"contact": "request"}, {"contact": "ready"}, {"not": {"contact": "fault"}}
]}}]}

class LadderTests(unittest.TestCase):
    def test_permissive_and_trace(self):
        inputs = {"request": True, "ready": True, "fault": False}
        result = scan(PROGRAM, inputs)
        self.assertTrue(result["outputs"]["run"])
        self.assertEqual(result, scan(PROGRAM, inputs))
        self.assertEqual(result["trace"][0]["coil"], "run")
        for key in inputs:
            changed = dict(inputs)
            changed[key] = not changed[key]
            self.assertFalse(scan(PROGRAM, changed)["outputs"]["run"])

    def test_rejects_missing_or_nonboolean(self):
        for inputs in ({"request": True, "ready": True}, {"request": 1, "ready": True, "fault": False}):
            with self.assertRaises(ProgramError):
                scan(PROGRAM, inputs)

    def test_rejects_duplicate_coil_and_unknown_operator(self):
        with self.assertRaises(ProgramError):
            scan({"version": 1, "rungs": PROGRAM["rungs"] * 2}, {})
        with self.assertRaises(ProgramError):
            scan({"version": 1, "rungs": [{"coil": "x", "expr": {"exec": "bad"}}]}, {})

    def test_or_branch(self):
        p = {"version": 1, "rungs": [{"coil": "x", "expr": {"any": [
            {"contact": "a"}, {"contact": "b"}]}}]}
        self.assertTrue(scan(p, {"a": False, "b": True})["outputs"]["x"])

if __name__ == "__main__":
    unittest.main()
