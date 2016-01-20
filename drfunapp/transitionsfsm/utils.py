# from transitions import Machine
# from transitions import HierarchicalMachine as Machine
from transitions_monkey_patches import Machine as Machine
from mimetypes import MimeTypes


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
        self['traffic3a'] = self.create_sample_machine_traffic_light_3state_1(**kwargs)
        self['traffic4a'] = self.create_sample_machine_traffic_light_4state_1(**kwargs)
        self['traffic4b'] = self.create_sample_machine_traffic_light_4state_2(**kwargs)
        self['traffic5a'] = self.create_sample_machine_traffic_light_2state3nested_1(**kwargs)
        self['traffic5b'] = self.create_sample_machine_traffic_light_2state3nested_2(**kwargs)
        self['traffic6a'] = self.create_sample_machine_traffic_light_2state4nested_1(**kwargs)
        self['traffic6b'] = self.create_sample_machine_traffic_light_2state4nested_2(**kwargs)
        # self['traffic'] = self.create_sample_machine_traffic_light_(**kwargs)

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
        # from transitions import HierarchicalMachine as Machine
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
        # from transitions import HierarchicalMachine as Machine
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

    def create_sample_machine_traffic_light_3state_1(self, **kwargs):
        states = ['green', 'yellow', 'red']
        order = ['green', 'yellow', 'red', 'green']
        m = Machine(states=states, initial='red', **kwargs)
        m.add_ordered_transitions(order)
        return m

    def create_sample_machine_traffic_light_4state_1(self, **kwargs):
        states = ['green', 'yellow', 'red', 'off']
        order = ['off', 'red', 'green', 'yellow', 'red']
        m = Machine(states=states, initial='red', **kwargs)
        m.add_ordered_transitions(order)
        return m

    def create_sample_machine_traffic_light_4state_2(self, **kwargs):
        transitions = [
            ['turned_on', 'off', 'red'],
            ['commence_shutdown', 'green', 'yellow'],
            ['poweroutage', '*', 'off']
        ]
        m = self.create_sample_machine_traffic_light_4state_1(transitions=transitions, **kwargs)
        return m

    def create_sample_machine_traffic_light_2state3nested_1(self, **kwargs):
        states = ['off', {'name': 'lit', 'children': ['green', 'yellow', 'red']}]
        order = ['off', 'lit_red', 'lit_green', 'lit_yellow', 'lit_red']
        transitions = [
            ['turned_on', 'off', 'lit_red'],
            ['commence_shutdown', 'lit_green', 'lit_yellow'],
            ['poweroutage', '*', 'off']
        ]
        m = Machine(states=states, transitions=transitions, initial='off', **kwargs)
        m.add_ordered_transitions(order)
        return m

    def create_sample_machine_traffic_light_2state3nested_2(self, **kwargs):
        states = ['off', {'name': 'lit', 'children': ['green', 'yellow', 'red']}]
        order = ['off', 'lit_red', 'lit_green', 'lit_yellow', 'lit_red']
        transitions = [
            ['turned_on', 'off', 'lit_red'],
            ['commence_shutdown', 'lit_green', 'lit_yellow'],
            # ['flash_on', 'off', ['lit_green', 'lit_yellow', 'lit_red']],
            ['flash_on_g', 'off', 'lit_green'],
            ['flash_on_y', 'off', 'lit_yellow'],
            ['flash_on_r', 'off', 'lit_red'],
            # ['flash_off', ['lit_green', 'lit_yellow', 'lit_red'], 'off'],
            ['flash_off_g', 'lit_green', 'off'],
            ['flash_off_y', 'lit_yellow', 'off'],
            ['flash_off_r', 'lit_red', 'off'],
            ['poweroutage', '*', 'off']
        ]
        m = Machine(states=states, transitions=transitions, initial='off', **kwargs)
        m.add_ordered_transitions(order)
        return m

    def create_sample_machine_traffic_light_2state4nested_1(self, **kwargs):
        states = [{'name': 'unlit', 'children': ['off', 'blank']}, {'name': 'lit', 'children': ['green', 'yellow', 'red']}]
        order = ['unlit_off', 'unlit_blank', 'lit_red', 'lit_green', 'lit_yellow', 'lit_red']
        transitions = [
            ['turned_on', 'unlit_off', 'unlit_blank'],
            ['commence_shutdown', 'lit_green', 'lit_yellow'],
            ['power_outage', '*', 'unlit_off']
        ]
        m = Machine(states=states, transitions=transitions, initial='unlit_off', **kwargs)
        m.add_ordered_transitions(order)
        return m

    def create_sample_machine_traffic_light_2state4nested_2(self, **kwargs):
        states = [{'name': 'unlit', 'children': ['off', 'blank']}, {'name': 'lit', 'children': ['green', 'yellow', 'red']}]
        order = ['unlit_off', 'unlit_blank', 'lit_red', 'lit_green', 'lit_yellow', 'lit_red']
        transitions = [
            ['turned_on', 'unlit_off', 'unlit_blank'],
            # ['flash_on', 'unlit_blank', ['lit_green', 'lit_yellow', 'lit_red']],
            ['flash_on_g', 'unlit_blank', 'lit_green'],
            ['flash_on_y', 'unlit_blank', 'lit_yellow'],
            ['flash_on_r', 'unlit_blank', 'lit_red'],
            # ['flash_off', ['lit_green', 'lit_yellow', 'lit_red'], 'unlit_blank'],
            ['flash_off_g', 'lit_green', 'unlit_blank'],
            ['flash_off_y', 'lit_yellow', 'unlit_blank'],
            ['flash_off_r', 'lit_red', 'unlit_blank'],
            ['commence_shutdown', 'lit_green', 'lit_yellow'],
            ['power_outage', '*', 'unlit_off']
        ]
        m = Machine(states=states, transitions=transitions, initial='unlit_off', **kwargs)
        m.add_ordered_transitions(order)
        return m


def _init_mimeutils_mime_types():
    obj = MimeTypes()
    # this is a special case since the DOT extension is normally mapped to 'application/msword'
    obj.add_type('text/plain', '.dot', True)
    # obj.add_type('text/plain', '.dot', False)
    return obj


class MimeUtils(object):
    _mime_types = _init_mimeutils_mime_types()

    @classmethod
    def get_mime_type(cls, ext, strict=True):
        if not ext:
            raise ValueError('Invalid value: ext.')

        ext = str(ext).lower()
        content_type = cls._mime_types.types_map[strict].get('.{}'.format(ext))
        if content_type:
            return content_type

        return 'text/plain'


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


def graph_machine(machine, title=None, image_format=None, layout_program=None):
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

    graph = machine.get_graph(title=title)
    # graph.layout()  # layout with default (neato)
    # graph.layout(prog=layout_program)
    # graph.draw('my_state_diagram.png', prog='dot')
    image = graph.draw(format=image_format, prog=layout_program)
    return image


def get_machine_dot(machine, title=None, layout_program=None):
    """
    Gets the 'DOT' source code for the graph of a FSM Machine.

    :param machine: The <transitions.Machine> to generate a graph image of.
    :param layout_program: The graphviz layout program to use.
        Possible values include: 'neato', 'dot', 'twopi', 'circo', 'fdp', 'nop', 'wc', 'acyclic', 'gvpr', 'gvcolor',
        'ccomps', 'sccmap', 'tred', 'sfdp'..
    :return:
    """
    layout_program = layout_program or 'dot'
    return graph_machine(machine=machine, title=title, layout_program=layout_program, image_format='dot')
    # layout_program = layout_program or 'dot'
    #
    # graph = machine.get_graph(title=title, diagram_class=BetterFSMGraph)
    # # graph.layout()  # layout with default (neato)
    # graph.layout(prog=layout_program)
    # return graph.to_dot()
