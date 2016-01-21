from six import string_types
from transitions import EventData
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
        # return str(self.summarize())
        return str(self.snapshot(verbose=False))

    def summarize(self):
        return summarize_machine(self)

    def get_graph(self, title=None, diagram_class=BetterFSMGraph):
        return super(Machine, self).get_graph(title, diagram_class)

    def trigger_transition(self, trigger, dest_state=None, source_state=None, *args, **kwargs):
        """
        Serially execute all transitions that match the specified transition criteria
        (triggering event (required); destination state (default is to match any destination state);
        source state (defaults to current state)), and returns as soon as any transition successfully executes.

        :param trigger: the name of the triggering Event (i.e. the name of the Transition action).
        :param dest_state: the name of the destination State.
            If unspecified, all States will be considered valid destination states.
        :param source_state: the name of the source State.
            Defaults to the Machine's current State.
        :param args: Optional positional arguments that will
                be passed onto the EventData object, enabling arbitrary state
                information to be passed on to downstream triggered functions
        :param kwargs: Optional named arguments that will
                be passed onto the EventData object, enabling arbitrary state
                information to be passed on to downstream triggered functions
        :return: the Transition that successfully executed (else None if no Transitions were successful).
        """
        ev = self.get_event(trigger)
        source_state = source_state or self.current_state
        transitions = self.get_transitions(event=ev, dest_state=dest_state, source_state=source_state)

        # transition = transitions[0]

        machine = ev.machine
        ev_data = EventData(machine.current_state, ev, machine,
                            machine.model, args=args, kwargs=kwargs)
        for t in transitions:
            ev_data.transition = t
            if t.execute(ev_data):
                return t
        return None

    # def trigger_transition(self, trigger, source_state=None, dest_state=None, *args, **kwargs):
    #     # get the callable trigger function
    #     trigger_function = getattr(self, dest_state)
    #
    #     # invoke the trigger function
    #     return trigger_function()

    def get_event(self, trigger):
        """

        :param trigger: the name of the Event triggering the Transition.
        :return: an Event, or None.
        """
        if isinstance(trigger, string_types):
            trigger_name = trigger
        else:
            trigger_name = trigger.name
        ev = self.events[trigger_name]
        return ev

    def get_transitions(self, event, dest_state=None, source_state=None):
        """

        :param event: the triggering Event instance.
        :param dest_state: the name of the destination State.
        :param source_state: the name of the source State.
        :return: a list of matching Transitions.
        """
        ev = event

        if source_state:
            if isinstance(source_state, string_types):
                source_state_name = source_state
            else:
                source_state_name = source_state.name
            # transitions = [t for t in ev.transitions if t.source == source_state_name]
            transitions = ev.transitions[source_state_name]
        else:
            transitions = ev.transitions.values()

        if dest_state:
            if isinstance(dest_state, string_types):
                dest_state_name = dest_state
            else:
                dest_state_name = dest_state.name
            transitions = [t for t in transitions if t.dest == dest_state_name]

        return transitions

    def snapshot(self, verbose=False):
        """
        Generates a hierarchical DOM representation of the Machine's current (object instance) state.

        :param verbose: if True, a 'full' snapshot will be returned.
            if False, a 'concise' snapshot will be returned.
            a 'concise' snapshot is often smaller and more readable than a verbose snapshot,
            but may (in comparison to a full snapshot) be incomplete and/or unsuitable for certain purposes.
        :return: a dict
        """
        return get_snapshot(self, verbose=verbose)


def get_snapshot(machine, verbose=False):
    """
    Generates a hierarchical DOM representation of the Machine's current (object instance) state.

    :param machine: the Machine to get a snapshot for.
    :param verbose: if True, a full snapshot will be returned.
        if False, a 'concise' snapshot will be returned.
        a 'concise' snapshot is often smaller and more readable than a verbose snapshot,
        but may (in comparison to a full snapshot) be incomplete and/or unsuitable for certain purposes.
    :return: a dict
    """
    default_send_event_ = False
    default_auto_transitions_ = True
    # default_ordered_transitions_ = False
    default_ignore_invalid_triggers_ = None
    # default_before_state_change_ = None
    # default_after_state_change_ = None

    m = machine

    d = dict()

    try:
        blueprints = m.blueprints
    except AttributeError:
        blueprints = None

    if blueprints:
        d.update(blueprints)
    else:
        # d.update({k: str(v) for k, v in m.__dict__.items()})
        d.update(summarize_machine(m))

    # noinspection PyProtectedMember
    d['initial'] = m._initial
    d['current'] = m.current_state.name
    if verbose or default_send_event_ != m.send_event:
        d['send_event'] = m.send_event
    if verbose or default_auto_transitions_ != m.auto_transitions:
        d['auto_transitions'] = m.auto_transitions
    if verbose or default_ignore_invalid_triggers_ != m.ignore_invalid_triggers:
        d['ignore_invalid_triggers'] = m.ignore_invalid_triggers
    # if verbose:
    #     d['model'] = m.model
    #     d['events'] = m.events
    #     d['before_state_change'] = m.before_state_change
    #     d['after_state_change'] = m.after_state_change

    if not verbose:
        d = filter_none_values(d)
        if 'transitions' in d:
            d['transitions'] = [filter_none_values(t) for t in d['transitions']]

    return d


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
    states = [summarize_state(s) for s in m.states]
    events = [summarize_event(e) for e in m.events]
    return filter_none_values({'states': states, 'events': events})


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
