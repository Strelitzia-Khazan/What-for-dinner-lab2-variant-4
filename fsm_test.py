# test.py
import unittest
from fsm import FSM

class TestFSM(unittest.TestCase):
    def setUp(self):
        self.fsm = FSM("Test FSM")
        self.fsm.add_state("Red", "Stop")
        self.fsm.add_state("Green", "Go")
        self.fsm.add_state("Yellow", "Caution")
        self.fsm.add_transition("Red", "Green", "timer")
        self.fsm.add_transition("Green", "Yellow", "timer")
        self.fsm.add_transition("Yellow", "Red", "timer")
        self.fsm.set_initial_state("Red")

    def test_initial_state(self):
        self.assertEqual(self.fsm.current_state.name, "Red")

    def test_state_transition(self):
        self.assertEqual(self.fsm.trigger_event("timer"), "Go")
        self.assertEqual(self.fsm.current_state.name, "Green")
        self.assertEqual(self.fsm.trigger_event("timer"), "Caution")
        self.assertEqual(self.fsm.current_state.name, "Yellow")
        self.assertEqual(self.fsm.trigger_event("timer"), "Stop")
        self.assertEqual(self.fsm.current_state.name, "Red")

    def test_invalid_event(self):
        with self.assertRaises(ValueError):
            self.fsm.trigger_event("invalid_event")

    def test_add_duplicate_state(self):
        with self.assertRaises(ValueError):
            self.fsm.add_state("Red", "Stop")

    def test_transition_with_invalid_state(self):
        with self.assertRaises(ValueError):
            self.fsm.add_transition("Red", "Blue", "timer")

    def test_reset(self):
        self.fsm.trigger_event("timer")
        self.fsm.trigger_event("timer")
        self.fsm.reset()
        self.assertEqual(self.fsm.current_state.name, "Red")

    def test_visualize(self):
        dot_output = self.fsm.visualize()
        self.assertIn("Red", dot_output)
        self.assertIn("Green", dot_output)
        self.assertIn("Yellow", dot_output)

    def test_as_markdown(self):
        md_output = self.fsm.as_markdown()
        self.assertIn("| Red | Stop |", md_output)
        self.assertIn("| Green | Go |", md_output)
        self.assertIn("| Yellow | Caution |", md_output)

def practical_example():
    fsm = FSM("Traffic Light Controller")

    fsm.add_state("Red", "Stop")
    fsm.add_state("Green", "Go")
    fsm.add_state("Yellow", "Caution")

    fsm.add_transition("Red", "Green", "timer")
    fsm.add_transition("Green", "Yellow", "timer")
    fsm.add_transition("Yellow", "Red", "timer")

    fsm.set_initial_state("Red")

    # 打印初始状态
    print(f"Initial State: {fsm.current_state.name} - Output: {fsm.current_state.output}")

    # 模拟状态转换
    events = ["timer", "timer", "timer", "timer", "timer"]
    for event in events:
        output = fsm.trigger_event(event)
        print(f"Event: {event}, New State: {fsm.current_state.name}, Output: {output}")

    # 可视化 FSM
    print("\nFSM Visualization in DOT format:")
    print(fsm.visualize())

    # 生成 Markdown 表格
    print("\nFSM in Markdown format:")
    print(fsm.as_markdown())

if __name__ == '__main__':
    unittest.main()
    practical_example()
