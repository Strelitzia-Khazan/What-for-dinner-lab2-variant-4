import logging
from collections import namedtuple

logging.basicConfig(level=logging.INFO)

state = namedtuple("state","clock current_state val")

class State:
    def __init__(self, name, output):
        self.name = name
        self.output = output

class Transition:
    def __init__(self, source, destination, latency):
        self.source = source
        self.destination = destination
        self.latency = latency

class FSM:
    def __init__(self, name):
        self.name = name
        self.clock = 0
        self.states = {}
        self.transitions = []
        self.initial_state = None
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
            raise ValueError("Both states must be added before creating a transition.")
        self.transitions.append(Transition(source, destination, latency))
        self.logger.info(f"Added transition from {source} to {destination} with {latency}")

    def set_initial_state(self, name):
        if name not in self.states:
            raise ValueError(f"State {name} has not been added.")
        self.initial_state = self.states[name]
        self.current_state = self.initial_state
        record = state(self.clock, self.current_state.name, self.current_state.output)
        self.state_history.append(record)
        self.logger.info(f"Set initial state to {name}")

    def trigger_event(self, event, latency):
        for transition in self.transitions:
            if transition.source == self.current_state.name:
                self.clock += latency
                record = state(self.clock, self.current_state.name, self.current_state.output)
                self.state_history.append(record)

                self.current_state = self.states[transition.destination]

                self.clock+=transition.latency
                record = state(self.clock, self.current_state.name, self.current_state.output)
                self.state_history.append(record)

                self.logger.info(f"Transitioned to {self.current_state.name} on event {event}")
                return self.current_state.output
        raise ValueError(f"No transition found from state {self.current_state.name} on event {event}")

    # def reset(self):
    #     self.current_state = self.initial_state
    #     self.state_history.append(self.current_state.name)
    #     self.logger.info("FSM reset to initial state")

    # def visualize(self):
    #     dot_repr = "digraph FSM {\n"
    #     for state in self.states.values():
    #         dot_repr += f'  {state.name} [label="{state.name}\\n{state.output}"];\n'
    #     for transition in self.transitions:
    #         dot_repr += f'  {transition.source} -> {transition.destination} [label="{transition.latency}"];\n'
    #     dot_repr += "}"
    #     return dot_repr

    def as_table(self):
        repr = "| State | Output |\n|-------|--------|\n"
        for state in self.states.values():
            repr += f"| {state.name} | {state.output} |\n"
        repr += "\n| Source | Latency | Destination |\n|--------|---------|-------------|\n"
        for transition in self.transitions:
            repr += f"| {transition.source} | {transition.latency} | {transition.destination} |\n"
        return repr

    def print_history(self):
        print("State History:")
        for record in self.state_history:
            print(f"Clock: {record.clock}, State: {record.current_state}, Output: {record.val}")


fsm = FSM("交通信号控制器")

fsm.add_state("Red", output="Stop")
fsm.add_state("Green", output="Go")
fsm.add_state("Yellow", output="Caution")

fsm.add_transition("Red", "Green", 1)
fsm.add_transition("Green", "Yellow", 1)
fsm.add_transition("Yellow", "Red", 1)

fsm.set_initial_state("Red")

print(fsm.trigger_event("timer", latency=1))  # 输出: Go
fsm.print_history()
print(fsm.trigger_event("timer", latency=1))  # 输出: Caution
print(fsm.trigger_event("timer", latency=1))  # 输出: Stop
print(fsm.trigger_event("timer", latency=1))  # 输出: Go
print(fsm.trigger_event("timer", latency=1))  # 输出: Caution

# fsm.print_history()

# # 以DOT格式可视化
# print(fsm.visualize())

# 以Markdown格式可视化
print(fsm.as_table())
