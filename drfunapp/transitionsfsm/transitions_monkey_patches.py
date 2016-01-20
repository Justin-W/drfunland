from transitions import HierarchicalMachine as OldMachine
from transitions.extensions import AAGraph as FsmGraph
from pygraphviz.agraph import AGraph as PgvGraph
try:
    import pygraphviz as pgv
except:
    pgv = None


class BetterPGVGraph(PgvGraph):
    def __init__(self, *args, **kwargs):
        super(BetterPGVGraph, self).__init__(*args, **kwargs)

    def to_dot(self, prog='neato', args=''):
        """
        Render the graph to Graphviz DOT format.
        """
        fmt = 'dot'
        data = self._run_prog(prog, ' '.join([args, "-T", fmt]))
        return data
        # self.from_string(data)
        # self.has_layout = True
        # return


class BetterFSMGraph(FsmGraph):
    def __init__(self, machine):
        super(BetterFSMGraph, self).__init__(machine)
        self.seen = []

    def get_graph(self, title=None):
        """ Generate a DOT graph with pygraphviz, returns an AGraph object
        Args:
            title (string): Optional title for the graph.
        """
        if not pgv:
            raise Exception('AGraph diagram requires pygraphviz')

        if title is None:
            title = self.__class__.__name__
        elif title is False:
            title = ''

        # fsm_graph = pgv.AGraph(label=title, **self.machine_attributes)
        fsm_graph = BetterPGVGraph(label=title, **self.machine_attributes)
        fsm_graph.node_attr.update(self.state_attributes)

        # For each state, draw a circle
        self._add_nodes(self.machine.states, fsm_graph)

        self._add_edges(self.machine.events, fsm_graph)

        return fsm_graph

    def to_dot(self, prog='neato', args=''):
        """
        Render the graph to Graphviz DOT format.
        """
        g = self.get_graph()
        return g.to_dot(prog=prog, args=args)


class Machine(OldMachine):
    def __init__(self, *args, **kwargs):
        super(Machine, self).__init__(*args, **kwargs)

    def __str__(self):
        return str(self.summarize())

    def summarize(self):
        return summarize_machine(self)

    def get_graph(self, title=None, diagram_class=BetterFSMGraph):
        return super(Machine, self).get_graph(title, diagram_class)


def filter_none_values(d):
    """
    Filters any keys with None values out of a dict.

    :param d: a dict
    :return: a dict comprehension
    """
    return {k: v for k, v in d.items() if v is not None}


def summarize_machine(m):
    """
    Generates a text representation of a FSM Machine.

    :param m: The <transitions.Machine> to summarize.
    """
    try:
        blueprints = m.blueprints
    except AttributeError:
        blueprints = None
        # blueprints = dir(m)
    states = [summarize_state(s) for s in m.states]
    events = [summarize_event(e) for e in m.events]
    return filter_none_values({'blueprints': blueprints, 'states': states, 'events': events})
    # return filter_none_values({'states': states, 'events': events})


def summarize_state(s):
    """
    Generates a text representation of a State.

    :param s: The <transitions.State> to summarize.
    """
    try:
        return filter_none_values({'name': s.name, 'on_enter': str(s.on_enter), 'on_exit': str(s.on_exit)})
    except AttributeError:
        return str(s)


def summarize_event(e):
    """
    Generates a text representation of a Event.

    :param e: The <transitions.Event> to summarize.
    """
    try:
        transitions = [summarize_transition(t, e.name) for t in e.transitions if t]
        return filter_none_values({'name': e.name, 'transitions': transitions})
    except AttributeError:
        return str(e)


def summarize_transition(t, trigger):
    """
    Generates a text representation of a Transition.

    :param t: The <transitions.Transition> to summarize.
    :param trigger: The trigger of the transition.
    """
    return filter_none_values({'source': t.source, 'dest': t.dest, 'trigger': trigger})
