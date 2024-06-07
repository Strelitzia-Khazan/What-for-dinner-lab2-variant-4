import unittest
from fsm import FSM, State


class TestFSM(unittest.TestCase):
    def setUp(self):
        self.fsm = FSM("Test FSM")
        self.fsm.add_state("Red", "Stop")
        self.fsm.add_state("Green", "Go")
        self.fsm.add_state("Yellow", "Caution")
        self.fsm.add_transition("Red", "Green", 1)
        self.fsm.add_transition("Green", "Yellow", 1)
        self.fsm.add_transition("Yellow", "Red", 1)
        self.fsm.set_initial_state("Red")

    def test_initial_state(self):
        self.assertEqual(self.fsm.current_state.name, "Red")
        self.assertEqual(self.fsm.clock, 0)

    def test_state_transition(self):
        self.assertEqual(self.fsm.trigger_event("timer", latency=1), "Go")
        self.assertEqual(self.fsm.current_state.name, "Green")
        self.assertEqual(self.fsm.clock, 2)
        self.assertEqual(self.fsm.trigger_event("timer", latency=1), "Caution")
        self.assertEqual(self.fsm.current_state.name, "Yellow")
        self.assertEqual(self.fsm.clock, 4)
        self.assertEqual(self.fsm.trigger_event("timer", latency=1), "Stop")
        self.assertEqual(self.fsm.current_state.name, "Red")
        self.assertEqual(self.fsm.clock, 6)

    def test_add_duplicate_state(self):
        with self.assertRaises(ValueError):
            self.fsm.add_state("Red", "Stop")

    def test_transition_with_invalid_state(self):
        with self.assertRaises(ValueError):
            self.fsm.add_transition("Red", "Blue", 1)

    # def test_visualize(self):
    #     dot_output = self.fsm.visualize()
    #     self.assertIn("Red", dot_output)
    #     self.assertIn("Green", dot_output)
    #     self.assertIn("Yellow", dot_output)

    # def test_as_markdown(self):
    #     md_output = self.fsm.as_markdown()
    #     self.assertIn("| Red | Stop |", md_output)
    #     self.assertIn("| Green | Go |", md_output)
    #     self.assertIn("| Yellow | Caution |", md_output)

    def test_as_table(self):
        expected_output = (
            "| State | Output |\n"
            "|-------|--------|\n"
            "| Red | Stop |\n"
            "| Green | Go |\n"
            "| Yellow | Caution |\n"
            "\n"
            "| Source | Latency | Destination |\n"
            "|--------|---------|-------------|\n"
            "| Red | 1 | Green |\n"
            "| Green | 1 | Yellow |\n"
            "| Yellow | 1 | Red |\n"
        )
        md_output = self.fsm.as_table()
        self.assertEqual(md_output.strip(), expected_output.strip())

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
        fsm.add_state("Green", "Go")
        fsm.add_state("Yellow", "Caution")

        fsm.add_transition("Red", "Green", 1)
        fsm.add_transition("Green", "Yellow", 1)
        fsm.add_transition("Yellow", "Red", 1)

        fsm.set_initial_state("Red")

        print(f"Initial State: {fsm.current_state.name} - Output: {fsm.current_state.output}")

        events = ["timer", "timer", "timer", "timer", "timer"]

        expected_results = [
            ("Green", "Go"),
            ("Yellow", "Caution"),
            ("Red", "Stop"),
            ("Green", "Go"),
            ("Yellow", "Caution")
        ]

        for event, expected in zip(events, expected_results):
            output = fsm.trigger_event(event, latency=1)
            self.assertEqual((fsm.current_state.name, output), expected)
            print(f"Event: {event}, New State: {fsm.current_state.name}, Output: {output}")

        fsm.print_history()


if __name__ == '__main__':
    unittest.main()