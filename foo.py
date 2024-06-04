import logging
from collections import OrderedDict, namedtuple
import copy

# 设置日志记录
logging.basicConfig(level=logging.INFO)

# 定义事件元组
Event = namedtuple("Event", "clock node var val")
SourceEvent = namedtuple("SourceEvent", "var val latency")

# 节点类
class Node(object):
    def __init__(self, name, function):
        self.function = function
        self.name = name
        self.inputs = OrderedDict()
        self.outputs = OrderedDict()

    def __repr__(self):
        return "{} inputs: {} outputs: {}".format(self.name, self.inputs, self.outputs)

    def input(self, name, latency=1):
        assert name not in self.inputs
        self.inputs[name] = latency

    def output(self, name, latency=1):
        assert name not in self.outputs
        self.outputs[name] = latency

    def activate(self, state):
        args = [state.get(v, None) for v in self.inputs]
        res = self.function(*args)
        if not isinstance(res, tuple):
            res = (res,)

        output_events = []
        for var, val in zip(self.outputs, res):
            latency = self.outputs[var]
            output_events.append(SourceEvent(var, val, latency))
        return output_events

# 离散事件模拟器类
class DiscreteEvent(object):
    def __init__(self, name="anonymous"):
        self.name = name
        self.inputs = OrderedDict()
        self.outputs = OrderedDict()
        self.nodes = []
        self.state_history = []
        self.event_history = []

    def input_port(self, name, latency=1):
        self.inputs[name] = latency

    def output_port(self, name, latency=1):
        self.outputs[name] = latency

    def add_node(self, name, function):
        node = Node(name, function)
        self.nodes.append(node)
        return node

    def _source_events2events(self, source_events, clock):
        events = []
        for se in source_events:
            source_latency = clock + se.latency + self.inputs.get(se.var, 0)
            if se.var in self.outputs:
                target_latency = self.outputs[se.var]
                events.append(Event(clock=source_latency + target_latency, node=None, var=se.var, val=se.val))
            for node in self.nodes:
                if se.var in node.inputs:
                    target_latency = node.inputs[se.var]
                    events.append(Event(clock=clock + source_latency + target_latency, node=node, var=se.var, val=se.val))
        return events

    def _pop_next_event(self, events):
        assert len(events) > 0
        events = sorted(events, key=lambda e: e.clock)
        event = events.pop(0)
        return event, events

    def _state_initialize(self):
        env = {var: None for var in self.inputs}
        return env

    def execute(self, *source_events, limit=100, events=None):
        if events is None:
            events = []
        state = self._state_initialize()
        clock = 0

        self.state_history = [(clock, copy.copy(state))]

        while (len(events) > 0 or len(source_events) > 0) and limit > 0:
            limit -= 1
            new_events = self._source_events2events(source_events, clock)
            events.extend(new_events)
            if len(events) == 0:
                break

            event, events = self._pop_next_event(events)
            state[event.var] = event.val
            clock = event.clock

            source_events = event.node.activate(state) if event.node else []

            self.state_history.append((clock, copy.copy(state)))
            self.event_history.append(event)

            logging.info(f"Event: {event} at clock: {clock}")
            logging.info(f"State: {state}")

        if limit == 0:
            logging.warning("Limit reached")
        return state

    def visualize(self):
        res = ["digraph G {", " rankdir=LR;"]
        for v in self.inputs:
            res.append(f" {v} [shape=rarrow];")
        for v in self.outputs:
            res.append(f" {v} [shape=rarrow];")
        for i, n in enumerate(self.nodes):
            res.append(f' n_{i} [label="{n.name}"];')
        for i, n in enumerate(self.nodes):
            for v in n.inputs:
                if v in self.inputs:
                    res.append(f' {v} -> n_{i};')
            for j, n2 in enumerate(self.nodes):
                if i == j:
                    continue
                for v in n.inputs:
                    if v in n2.outputs:
                        res.append(f' n_{j} -> n_{i} [label="{v}"];')
            for v in n.outputs:
                if v in self.outputs:
                    res.append(f' n_{i} -> {v};')
        res.append("}")
        return "\n".join(res)

    def to_markdown(self):
        md = ["| Clock | State |", "| --- | --- |"]
        for clock, state in self.state_history:
            state_str = ", ".join(f"{k}: {v}" for k, v in state.items())
            md.append(f"| {clock} | {state_str} |")
        return "\n".join(md)

# 示例：交通灯控制器
def traffic_light_controller():
    fsm = DiscreteEvent("TrafficLight")

    fsm.input_port("clock", latency=0)
    fsm.output_port("light", latency=1)

    green = fsm.add_node("green", lambda clock: ("green",))
    yellow = fsm.add_node("yellow", lambda clock: ("yellow",))
    red = fsm.add_node("red", lambda clock: ("red",))

    green.output("light", latency=0)
    yellow.output("light", latency=0)
    red.output("light", latency=0)

    green.input("clock", latency=5)
    yellow.input("clock", latency=2)
    red.input("clock", latency=7)

    fsm.execute(SourceEvent("clock", 0, 0))

    print("State History:")
    print(fsm.to_markdown())
    print("\nState Diagram:")
    print(fsm.visualize())

traffic_light_controller()
