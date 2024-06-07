# fsm.py
import logging
from collections import namedtuple

logging.basicConfig(level=logging.INFO)

state = namedtuple("state", "clock current_state val")


class State:
    def __init__(self, name, output):
        self.name = name
        self.output = output


class Transition:
    def __init__(self, source, destination, latency, fsm):
        self.source = source
        self.destination = destination
        self.latency = latency
        self.output = fsm.states[source].output


class FSM:
    def __init__(self, name):
        self.name = name
        self.clock = 0
        self.states = {}
        self.transitions = []
        self.current_state = None
        self.state_history = []
        self.logger = logging.getLogger(name)

    def add_state(self, name, output):
        if name in self.states:
            raise ValueError(f"State {name} already exists.")
        self.states[name] = State(name, output)
        self.logger.info(f"Added state {name} with output {output}")

    def add_transition(self, source, destination, latency):
        if source not in self.states or destination not in self.states:
            raise ValueError("Add states frist.")
        self.transitions.append(Transition(source, destination, latency, self))
        self.logger.info(
            f"Added transition from "
            f"{source} to {destination} with {latency}"
        )

    def set_initial_state(self, name):
        if name not in self.states:
            raise ValueError(f"State {name} has not been added.")
        self.current_state = self.states[name]
        record = state(self.clock, 
                       self.current_state.name, 
                       self.current_state.output)
        self.state_history.append(record)
        self.logger.info(f"Set initial state to {name}")

    def trigger_event(self, event, latency):
        for transition in self.transitions:
            if transition.source == self.current_state.name:
                self.clock += latency
                record = state(self.clock, 
                               self.current_state.name, 
                               self.current_state.output)
                self.state_history.append(record)
                self.current_state = self.states[transition.destination]
                self.clock+=transition.latency
                record = state(self.clock, 
                               self.current_state.name, 
                               self.current_state.output)
                self.state_history.append(record)
                self.logger.info(
                    f"Transitioned to {self.current_state.name} "
                    f"on event {event}"
                )
                return self.current_state.output
        raise ValueError(
            f"No transition found from state "
            f"{self.current_state.name} on event {event}"
        )

    def visualize_dot(self):
        dot_repr = "digraph Moore FSM {\n"
        # Define the nodes with their outputs
        for state_name, state in self.states.items():
            dot_repr += f'    {state_name} [label="Output={state.output}"];\n'
        # Define the transitions with their latencies
        for transition in self.transitions:
            dot_repr += (
                f'    {transition.source} -> {transition.destination} '
                f'[label="Output={transition.output} / Latency={transition.latency}"];\n'
            )
        dot_repr += "}"
        return dot_repr

    def visualize_markdown(self):
        md_repr = "| State | Output |\n|-------|--------|\n"
        for state in self.states.values():
            md_repr += f"| {state.name} | {state.output} |\n"
        md_repr += "\n| Source | Destination | Output | Latency |\n"
        md_repr += "|--------|-------------|--------|---------|\n"
        for transition in self.transitions:
            md_repr += (
                f"| {transition.source} "
                f"| {transition.destination} "
                f"| {transition.output} "
                f"| {transition.latency} |\n"
            )
        return md_repr

    def print_history(self):
        print("State History:")
        for record in self.state_history:
            print(f"Clock: {record.clock}, "
                  f"State: {record.current_state}, "
                  f"Output: {record.val}")
