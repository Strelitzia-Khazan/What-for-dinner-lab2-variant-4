from typing import Dict, Optional, Tuple, List, Any

class Node:
    def __init__(self, name: str, transition_rules: Dict[int, str], output_mapping: Dict[int, Tuple[str, int]]) -> None:
        self.name: str = name
        self.transition_rules: Dict[int, str] = transition_rules
        self.output_mapping: Dict[int, Tuple[str, int]] = output_mapping

    def activate(self, input_tuple: Tuple[int, Any]) -> Tuple[str, Optional[Tuple[str, int]]]:
        time, input_value = input_tuple
        if input_value in self.transition_rules:
            next_state = self.transition_rules[input_value]
            output_with_latency = self.output_mapping.get(input_value)
            return next_state, output_with_latency
        else:
            return self.name, None

class MooreFSM:
    def __init__(self, initial_state: str) -> None:
        self.current_state: str = initial_state
        self.nodes: Dict[str, Node] = {}
        self.state_seq: List[Tuple[int, str]] = []
        self.output_seq: List[Tuple[int, Tuple[str, int]]] = []

    def add_node(self, node_name: str, transition_rules: Dict[int, str], output_mapping: Dict[int, Tuple[str, int]]) -> None:
        node: Node = Node(node_name, transition_rules, output_mapping)
        self.nodes[node_name] = node

    def execute(self, input_seq: List[Tuple[int, Any]]) -> None:
        for input_tuple in input_seq:
            node: Node = self.nodes[self.current_state]
            next_state, output_with_latency = node.activate(input_tuple)
            self.state_seq.append((input_tuple[0], next_state))
            if output_with_latency is not None:
                self.output_seq.append((input_tuple[0], output_with_latency))
            self.current_state = next_state

    def visualize_dot(self) -> str:
        dot_graph = "digraph MooreFSM {\n"
        for node_name, node in self.nodes.items():
            for input_value, next_state in node.transition_rules.items():
                output_with_latency = node.output_mapping.get(input_value)
                output = output_with_latency[0] if output_with_latency is not None else ""
                latency = output_with_latency[1] if output_with_latency is not None else 0
                dot_graph += f'    {node_name} -> {next_state} [label="{input_value} / {output} / {latency}"];\n'
        dot_graph += "}"
        return dot_graph

    def visualize_markdown(self) -> str:
        table = "| Current State | Input | Next State | Output | Latency |\n"
        table += "|---------------|-------|------------|--------|---------|\n"
        for node_name, node in self.nodes.items():
            for input_value, next_state in node.transition_rules.items():
                output_with_latency = node.output_mapping.get(input_value)
                output = output_with_latency[0] if output_with_latency is not None else ""
                latency = output_with_latency[1] if output_with_latency is not None else 0
                table += f"| {node_name} | {input_value} | {next_state} | {output} | {latency} |\n"
        return table

# Create a MooreFSM instance
traffic_light_controller = MooreFSM(initial_state="Red")

# Add nodes for each state of the traffic light
traffic_light_controller.add_node(
    node_name="Red",
    transition_rules={1: "Green"},  # Transition from Red to Green when input 1 is received
    output_mapping={1: ("Stop", 1)}  # Output "Stop" with latency 1 when input 1 is received
)
traffic_light_controller.add_node(
    node_name="Green",
    transition_rules={2: "Yellow"},  # Transition from Green to Yellow when input 2 is received
    output_mapping={2: ("Go", 1)}  # Output "Go" with latency 1 when input 2 is received
)
traffic_light_controller.add_node(
    node_name="Yellow",
    transition_rules={3: "Red"},  # Transition from Yellow to Red when input 3 is received
    output_mapping={3: ("Caution", 1)}  # Output "Caution" with latency 1 when input 3 is received
)

# Define the input sequence for the traffic light controller
input_sequence = [
    (1, None),  # Input 1 received, transition from Red to Green
    (2, None),  # Input 2 received, transition from Green to Yellow
    (3, None),  # Input 3 received, transition from Yellow to Red
]

# Execute the input sequence
traffic_light_controller.execute(input_sequence)

# Visualize the state transition as DOT
print(traffic_light_controller.visualize_dot())

# Visualize the state transition as MarkDown
print(traffic_light_controller.visualize_markdown())
