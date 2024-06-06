import logging

logging.basicConfig(level=logging.INFO)

class State:
    def __init__(self, name, output):
        self.name = name
        self.output = output

class Transition:
    def __init__(self, source, destination, event):
        self.source = source
        self.destination = destination
        self.event = event

class FSM:
    def __init__(self, name):
        self.name = name
        self.states = {}
        self.transitions = []
        self.initial_state = None
        self.current_state = None
        self.logger = logging.getLogger(name)

    def add_state(self, name, output):
        if name in self.states:
            raise ValueError(f"State {name} already exists.")
        self.states[name] = State(name, output)
        self.logger.info(f"Added state {name} with output {output}")

    def add_transition(self, source, destination, event):
        if source not in self.states or destination not in self.states:
            raise ValueError("Both states must be added before creating a transition.")
        self.transitions.append(Transition(source, destination, event))
        self.logger.info(f"Added transition from {source} to {destination} on event {event}")

    def set_initial_state(self, name):
        if name not in self.states:
            raise ValueError(f"State {name} has not been added.")
        self.initial_state = self.states[name]
        self.current_state = self.initial_state
        self.logger.info(f"Set initial state to {name}")

    def trigger_event(self, event):
        for transition in self.transitions:
            if transition.source == self.current_state.name and transition.event == event:
                self.current_state = self.states[transition.destination]
                self.logger.info(f"Transitioned to {self.current_state.name} on event {event}")
                return self.current_state.output
        raise ValueError(f"No transition found from state {self.current_state.name} on event {event}")

    def reset(self):
        self.current_state = self.initial_state
        self.logger.info("FSM reset to initial state")

    def visualize(self):
        dot_repr = "digraph FSM {\n"
        for state in self.states.values():
            dot_repr += f'  {state.name} [label="{state.name}\\n{state.output}"];\n'
        for transition in self.transitions:
            dot_repr += f'  {transition.source} -> {transition.destination} [label="{transition.event}"];\n'
        dot_repr += "}"
        return dot_repr

    def as_markdown(self):
        md_repr = "| State | Output |\n|-------|--------|\n"
        for state in self.states.values():
            md_repr += f"| {state.name} | {state.output} |\n"
        md_repr += "\n| Source | Event | Destination |\n|--------|-------|-------------|\n"
        for transition in self.transitions:
            md_repr += f"| {transition.source} | {transition.event} | {transition.destination} |\n"
        return md_repr


fsm = FSM("交通信号控制器")

fsm.add_state("Red", output="Stop")
fsm.add_state("Green", output="Go")
fsm.add_state("Yellow", output="Caution")

fsm.add_transition("Red", "Green", "timer")
fsm.add_transition("Green", "Yellow", "timer")
fsm.add_transition("Yellow", "Red", "timer")

fsm.set_initial_state("Red")

print(fsm.trigger_event("timer"))  # 输出: Go
print(fsm.trigger_event("timer"))  # 输出: Caution
print(fsm.trigger_event("timer"))  # 输出: Stop
print(fsm.trigger_event("timer"))  # 输出: Go
print(fsm.trigger_event("timer"))  # 输出: Caution


# 以DOT格式可视化
print(fsm.visualize())

# 以Markdown格式可视化
print(fsm.as_markdown())