# from rest_framework import serializers
# from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response
# from rest_framework.reverse import reverse
# import requests as r4h
from transitions import Machine


# from transitions import HierarchicalMachine as Machine


class MachineCatalog(dict):
    def __init__(self, **kwargs):
        super(MachineCatalog, self).__init__(**kwargs)
        # self.preload(**kwargs)

    def preload(self, **kwargs):
        self['ordered'] = self.create_sample_machine_ordered(**kwargs)
        self['ordered2'] = self.create_sample_machine_ordered2(**kwargs)
        self['matter'] = self.create_sample_machine_matter(**kwargs)
        self['matter2'] = self.create_sample_machine_matter2(**kwargs)
        self['matter3'] = self.create_sample_machine_matter3(**kwargs)
        self['nested'] = self.create_sample_machine_nested(**kwargs)
        self['reuse'] = self.create_sample_machine_reuse(**kwargs)
        self['terms'] = self.create_sample_machine_terms(**kwargs)

    def create_sample_machine(self, name=None, **kwargs):
        if not name or name in ('a', 'terms'):
            return self.create_sample_machine_terms(**kwargs)
        elif name in ('b', 'ordered'):
            return self.create_sample_machine_ordered(**kwargs)
        elif name in ('b', 'ordered2'):
            return self.create_sample_machine_ordered2(**kwargs)
        elif name in ('c', 'matter'):
            return self.create_sample_machine_matter(**kwargs)
        elif name in ('c2', 'matter2'):
            return self.create_sample_machine_matter2(**kwargs)
        elif name in ('c3', 'matter3'):
            return self.create_sample_machine_matter3(**kwargs)
        elif name in ('d', 'nested'):
            return self.create_sample_machine_nested(**kwargs)
        elif name in ('e', 'reuse'):
            return self.create_sample_machine_reuse(**kwargs)

    def create_sample_machine_terms(self, **kwargs):
        # define our states and transitions
        states = ['consent', 'demographics', 'personality', 'task']
        transitions = [
            {
                'trigger': 'advance',
                'source': 'consent',
                'dest': 'demographics',
                'conditions': 'user_agrees'
            },
            {
                'trigger': 'advance',
                'source': 'demographics',
                'dest': 'personality',
                'conditions': 'validate_demographics',
                'before': 'save_demographics'
            },
            {
                'trigger': 'advance',
                'source': 'personality',
                'dest': 'task',
                'conditions': 'no_more_items',
                'before': 'save_items'
            }
        ]
        # Initialize the state machine with the above states and transitions, and start out life in the solid state.
        return Machine(states=states, transitions=transitions, initial='consent', **kwargs)

    def create_sample_machine_ordered(self, **kwargs):
        states = ['A', 'B', 'C']
        # See the "alternative initialization" section for an explanation of the 1st argument to init
        machine = Machine(None, states, initial='A', **kwargs)
        machine.add_ordered_transitions()
        # machine.next_state()
        # print(machine.state)
        # # >>> 'B'
        return machine

    def create_sample_machine_ordered2(self, **kwargs):
        # We can also define a different order of transitions
        states = ['A', 'B', 'C']
        machine = Machine(None, states, initial='A', **kwargs)
        machine.add_ordered_transitions(['A', 'C', 'B'])
        return machine

    def create_sample_machine_matter(self, **kwargs):
        states = ['solid', 'liquid', 'gas', 'plasma']

        # And some transitions between states. We're lazy, so we'll leave out
        # the inverse phase transitions (freezing, condensation, etc.).
        transitions = [
            {'trigger': 'melt', 'source': 'solid', 'dest': 'liquid'},
            {'trigger': 'evaporate', 'source': 'liquid', 'dest': 'gas'},
            {'trigger': 'sublimate', 'source': 'solid', 'dest': 'gas'},
            {'trigger': 'ionize', 'source': 'gas', 'dest': 'plasma'}
        ]

        # transitions = [
        #     ['melt', 'solid', 'liquid'],
        #     ['evaporate', 'liquid', 'gas'],
        #     ['sublimate', 'solid', 'gas'],
        #     ['ionize', 'gas', 'plasma']
        # ]

        # transitions = [
        #     {'trigger': 'melt', 'source': 'solid', 'dest': 'liquid'},
        #     {'trigger': 'evaporate', 'source': 'liquid', 'dest': 'gas'},
        #     {'trigger': 'sublimate', 'source': 'solid', 'dest': 'gas'},
        #     {'trigger': 'ionize', 'source': 'gas', 'dest': 'plasma'}
        # ]

        # Initialize
        # machine = Machine(model=Matter(), states=states, transitions=transitions, **kwargs)
        machine = Machine(states=states, transitions=transitions, initial='liquid', **kwargs)

        return machine

    def create_sample_machine_matter2(self, **kwargs):
        machine = self.create_sample_machine_matter(**kwargs)

        machine.add_transition('transmogrify', ['solid', 'liquid', 'gas'], 'plasma')

        machine.add_transition('transmogrify', 'plasma', 'solid')
        # This next transition will never execute
        machine.add_transition('transmogrify', 'plasma', 'gas')

        return machine

    def create_sample_machine_matter3(self, **kwargs):
        machine = self.create_sample_machine_matter(**kwargs)

        states = ['solid', 'liquid', 'gas', 'plasma']
        # states = machine.states
        machine.add_ordered_transitions(states)

        return machine

    def create_sample_machine_nested(self, **kwargs):
        from transitions import HierarchicalMachine as Machine
        # from transitions import NestedState as State

        states = ['standing', 'walking', {'name': 'caffeinated', 'children': ['dithering', 'running']}]
        transitions = [
            ['walk', 'standing', 'walking'],
            ['stop', 'walking', 'standing'],
            ['drink', '*', 'caffeinated'],
            ['walk', 'caffeinated_dithering', 'caffeinated_running'],
            ['relax', 'caffeinated', 'standing']
        ]
        machine = Machine(states=states, transitions=transitions, initial='standing', **kwargs)

        return machine

    def create_sample_machine_reuse(self, **kwargs):
        from transitions import HierarchicalMachine as Machine
        # from transitions import NestedState as State

        count_states = ['1', '2', '3', 'done']
        count_trans = [
            ['increase', '1', '2'],
            ['increase', '2', '3'],
            ['decrease', '3', '2'],
            ['decrease', '2', '1'],
            ['done', '3', 'done'],
            ['reset', '*', '1']
        ]

        counter = Machine(states=count_states, transitions=count_trans, initial='1', **kwargs)

        states = ['waiting', 'collecting', {'name': 'counting', 'children': counter}]
        # states = ['waiting', 'collecting', {'name': 'counting', 'children':counter.blueprints}]

        transitions = [
            ['collect', '*', 'collecting'],
            ['wait', '*', 'waiting'],
            ['count', 'waiting', 'counting']
        ]

        collector = Machine(states=states, transitions=transitions, initial='waiting', **kwargs)

        return collector


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


def graph_machine(machine, image_format=None, layout_program=None):
    """
    Generates an image of the graph of a FSM Machine.

    :param machine: The <transitions.Machine> to generate a graph image of.
    :param image_format:
        Possible values include: 'png', 'svg'.
    :param layout_program: The graphviz layout program to use.
        Possible values include: 'neato', 'dot', 'twopi', 'circo', 'fdp', 'nop', 'wc', 'acyclic', 'gvpr', 'gvcolor',
        'ccomps', 'sccmap', 'tred', 'sfdp'..
    :return:
    """
    layout_program = layout_program or 'neato'
    image_format = image_format or 'png'

    graph = machine.get_graph()
    # graph.layout()  # layout with default (neato)
    graph.layout(prog=layout_program)  # layout with default (neato)
    # graph.draw('my_state_diagram.png', prog='dot')
    image = graph.draw(format=image_format)
    return image
