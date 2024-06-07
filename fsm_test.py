import unittest
from fsm import FSM, State


class TestFSM(unittest.TestCase):
    def setUp(self):
        self.fsm = FSM("Test FSM")
        self.fsm.add_state("Red", "Stop")
        self.fsm.add_state("Green1", "Go")
        self.fsm.add_state("Green2", "Go")
        self.fsm.add_state("Green3", "Go")
        self.fsm.add_state("Yellow", "Caution")
        self.fsm.add_transition("Red", "Green1", 1)
        self.fsm.add_transition("Green1", "Green2", 1)
        self.fsm.add_transition("Green2", "Green3", 1)
        self.fsm.add_transition("Green3", "Yellow", 1)
        self.fsm.add_transition("Yellow", "Red", 1)
        self.fsm.set_initial_state("Red")

    def test_initial_state(self):
        self.assertEqual(self.fsm.current_state.name, "Red")
        self.assertEqual(self.fsm.clock, 0)

    def test_state_transition(self):
        self.assertEqual(self.fsm.trigger_event("timer", latency=1), "Go")
        self.assertEqual(self.fsm.current_state.name, "Green1")
        self.assertEqual(self.fsm.clock, 2)
        self.assertEqual(self.fsm.trigger_event("timer", latency=1), "Go")
        self.assertEqual(self.fsm.current_state.name, "Green2")
        self.assertEqual(self.fsm.clock, 4)
        self.assertEqual(self.fsm.trigger_event("timer", latency=1), "Go")
        self.assertEqual(self.fsm.current_state.name, "Green3")
        self.assertEqual(self.fsm.clock, 6)
        self.assertEqual(self.fsm.trigger_event("timer", latency=1), "Caution")
        self.assertEqual(self.fsm.current_state.name, "Yellow")
        self.assertEqual(self.fsm.clock, 8)
        self.assertEqual(self.fsm.trigger_event("timer", latency=1), "Stop")
        self.assertEqual(self.fsm.current_state.name, "Red")
        self.assertEqual(self.fsm.clock, 10)

    def test_add_duplicate_state(self):
        with self.assertRaises(ValueError):
            self.fsm.add_state("Red", "Stop")

    def test_transition_with_invalid_state(self):
        with self.assertRaises(ValueError):
            self.fsm.add_transition("Red", "Blue", 1)

    def test_visualize_dot(self):
        excepted_output = """digraph Moore FSM {
    Red [label="Output=Stop"];
    Green1 [label="Output=Go"];
    Green2 [label="Output=Go"];
    Green3 [label="Output=Go"];
    Yellow [label="Output=Caution"];
    Red -> Green1 [label="Output=Stop / Latency=1"];
    Green1 -> Green2 [label="Output=Go / Latency=1"];
    Green2 -> Green3 [label="Output=Go / Latency=1"];
    Green3 -> Yellow [label="Output=Go / Latency=1"];
    Yellow -> Red [label="Output=Caution / Latency=1"];
}"""
        dot_output = self.fsm.visualize_dot()
        self.assertEqual(dot_output, excepted_output)

    def test_visualize_markdown(self):
        expected_output = """| State | Output |
|-------|--------|
| Red | Stop |
| Green1 | Go |
| Green2 | Go |
| Green3 | Go |
| Yellow | Caution |

| Source | Destination | Output | Latency |
|--------|-------------|--------|---------|
| Red | Green1 | Stop | 1 |
| Green1 | Green2 | Go | 1 |
| Green2 | Green3 | Go | 1 |
| Green3 | Yellow | Go | 1 |
| Yellow | Red | Caution | 1 |
"""
        md_output = self.fsm.visualize_markdown()
        self.assertEqual(md_output, expected_output)

    def test_history(self):
        self.fsm.trigger_event("timer", latency=1)
        self.fsm.trigger_event("timer", latency=1)
        self.fsm.trigger_event("timer", latency=1)
        expected_state_history = [
            (0, "Red", "Stop"),
            (1, "Red", "Stop"),
            (2, "Green", "Go"),
            (3, "Green", "Go"),
            (4, "Yellow", "Caution"),
            (5, "Yellow", "Caution"),
            (6, "Red", "Stop")
        ]
        self.assertEqual([(record.clock, record.current_state, record.val) for record in self.fsm.state_history], expected_state_history)

    def test_practical_example(self):
        fsm = FSM("Traffic Light Controller")

        fsm.add_state("Red", "Stop")
        fsm.add_state("Green1", output="Go")
        fsm.add_state("Green2", output="Go")
        fsm.add_state("Green3", output="Go")
        fsm.add_state("Yellow", "Caution")

        fsm.add_transition("Red", "Green1", 1)
        fsm.add_transition("Green1","Green2", 1)
        fsm.add_transition("Green2","Green3", 1)
        fsm.add_transition("Green3", "Yellow", 1)
        fsm.add_transition("Yellow", "Red", 1)

        fsm.set_initial_state("Red")

        print(f"Initial State: {fsm.current_state.name} - Output: {fsm.current_state.output}")

        events = ["timer", "timer", "timer", "timer", "timer", "timer", "timer"]

        expected_results = [
            ("Green1", "Go"),
            ("Green2", "Go"),
            ("Green3", "Go"),
            ("Yellow", "Caution"),
            ("Red", "Stop"),
            ("Green1", "Go"),
            ("Green2", "Go")
        ]

        for event, expected in zip(events, expected_results):
            output = fsm.trigger_event(event, latency=1)
            self.assertEqual((fsm.current_state.name, output), expected)
            print(f"Event: {event}, New State: {fsm.current_state.name}, Output: {output}")

        fsm.print_history()


if __name__ == '__main__':
    unittest.main()