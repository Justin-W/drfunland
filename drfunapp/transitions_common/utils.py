# from transitions import Machine
# from transitions import HierarchicalMachine as Machine
import logging
from mimetypes import MimeTypes

from transitions_common.transitions_extensions import Machine as Machine


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
        self['task'] = self.create_sample_machine_task(**kwargs)
        self['terms'] = self.create_sample_machine_terms(**kwargs)
        self['traffic3a'] = self.create_sample_machine_traffic_light_3state_1(**kwargs)
        self['traffic4a'] = self.create_sample_machine_traffic_light_4state_1(**kwargs)
        self['traffic4b'] = self.create_sample_machine_traffic_light_4state_2(**kwargs)
        self['traffic5a'] = self.create_sample_machine_traffic_light_2state3nested_1(**kwargs)
        self['traffic5b'] = self.create_sample_machine_traffic_light_2state3nested_2(**kwargs)
        self['traffic6a'] = self.create_sample_machine_traffic_light_2state4nested_1(**kwargs)
        self['traffic6b'] = self.create_sample_machine_traffic_light_2state4nested_2(**kwargs)

    # def create_sample_machine(self, name=None, **kwargs):
    #     if not name or name in ('a', 'terms'):
    #         return self.create_sample_machine_terms(**kwargs)
    #     elif name in ('b', 'ordered'):
    #         return self.create_sample_machine_ordered(**kwargs)
    #     elif name in ('b', 'ordered2'):
    #         return self.create_sample_machine_ordered2(**kwargs)
    #     elif name in ('c', 'matter'):
    #         return self.create_sample_machine_matter(**kwargs)
    #     elif name in ('c2', 'matter2'):
    #         return self.create_sample_machine_matter2(**kwargs)
    #     elif name in ('c3', 'matter3'):
    #         return self.create_sample_machine_matter3(**kwargs)
    #     elif name in ('d', 'nested'):
    #         return self.create_sample_machine_nested(**kwargs)
    #     elif name in ('e', 'reuse'):
    #         return self.create_sample_machine_reuse(**kwargs)

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

        # NOTE: the 2 statements below are functionally equivalent to the 1 above

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

    def create_sample_machine_task(self, **kwargs):
        states = ['Unstarted', 'In Progress', 'Completed', 'Cancelled']
        order = ['Unstarted', 'In Progress', 'Completed']
        transitions = [
            ['Start', 'Unstarted', 'In Progress'],
            ['Complete', 'In Progress', 'Completed'],
            ['Cancel', 'In Progress', 'Cancelled']
        ]
        initial = states[0]

        machine = Machine(states=states, transitions=transitions, initial=initial, **kwargs)
        machine.add_ordered_transitions(order)

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


class LogUtils(object):
    # _logger = logging.Logger('LogUtils', level=logging.DEBUG)

    # @classmethod
    # def new_logger(cls, ext, strict=True):
    #     if not ext:
    #         raise ValueError('Invalid value: ext.')
    #
    #     ext = str(ext).lower()
    #     content_type = cls._mime_types.types_map[strict].get('.{}'.format(ext))
    #     if content_type:
    #         return content_type
    #
    #     return 'text/plain'

    @classmethod
    def log_object_state(cls, obj, name=None, context=None, level=None):
        from pprint import pformat
        info = dict()

        # funcs = [type, dir, vars, str, repr]
        # for f in funcs:
        #     # info[f.__name__] = f(obj)
        #     # info[inspect.getmembers(f).__name__] = f(obj)
        #     info[f.f_code.co_name] = f(obj)

        info['type'] = type(obj)
        # info['dir'] = dir(obj)
        try:
            info['vars'] = vars(obj)
        except TypeError:
            pass
        info['str'] = str(obj)
        info['repr'] = repr(obj)

        # info['inspect.getmembers'] = inspect.getmembers(obj)

        name_msg = ' (name: {name})'.format(name=name) if name else ''
        context_msg = ' (context: {context})'.format(context=context) if context else ''
        # state = pprint(info)
        # state = pprint(dict(info.items()))
        state = pformat(dict(info.items()))
        # state = json.dumps(info, indent=2)
        # state = repr(info)
        # state = repr(dict(info.items()))
        # state = json.dumps(info, indent=2)
        msg = 'Object State{name}{context}: {state}.'.format(name=name_msg, context=context_msg, state=state)
        level = level or logging.DEBUG
        logging.log(level=level, msg=msg)


def graph_machine(machine, title=None, image_format=None, layout_program=None):
    """
    Generates an image of the graph of a FSM Machine.

    :param machine: The <transitions.Machine> to generate a graph image of.
    :param title: The text of the graph's title label.
    :param image_format: The desired image/file format of the output.
        The set of valid values is determined by the version of graphviz you are using.
        Some examples of possible values (copied from graphviz output on different test environments) are shown below.
        Note that each of the example sets below includes some values not present in other sets.

        1. 'bmp', 'canon', 'cgimage', 'cmap', 'cmapx', 'cmapx_np', 'dot',
        'eps', 'exr', 'fig', 'gif', 'gv', 'icns', 'ico', 'imap', 'imap_np', 'ismap', 'jp2', 'jpe', 'jpeg', 'jpg',
        'pct', 'pdf', 'pic', 'pict', 'plain', 'plain-ext', 'png', 'pov', 'ps', 'ps2', 'psd', 'sgi', 'svg', 'svgz',
        'tga', 'tif', 'tiff', 'tk', 'vml', 'vmlz', 'xdot', 'xdot1.2', 'xdot1.4'

        2. 'canon', 'cmap', 'cmapx', 'cmapx_np', 'dot',
        'eps', 'fig', 'gd', 'gd2', 'gif', 'gv', 'imap', 'imap_np', 'ismap', 'jpe', 'jpeg', 'jpg',
        'pdf', 'plain', 'plain-ext', 'png', 'ps', 'ps2', 'svg', 'svgz',
        'tk', 'vml', 'vmlz', 'vrml', 'wbmp', 'x11', 'xdot', 'xlib'
    :param layout_program: The graphviz layout program to use.
        The set of valid values is determined by the version of graphviz you are using.
        Some examples of possible values (copied from graphviz output on different test environments) are shown below.

        1. 'neato', 'dot', 'twopi', 'circo', 'fdp', 'nop', 'wc', 'acyclic', 'gvpr', 'gvcolor',
        'ccomps', 'sccmap', 'tred', 'sfdp'
    :return:
    """
    layout_program = layout_program or 'neato'
    image_format = image_format or 'png'

    graph = machine.get_graph(title=title)
    output = graph.draw(format=image_format, prog=layout_program)
    return output


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


def kwargs_merge(kwargs_explicit, kwargs_defaults):
    """
    Combines two 'kwargs'-type instances into a single kwargs.

    E.g. Useful for merging caller-specified kwargs with a set of 'default' kwargs
    (with values that may or may not overlap with each other).

    :param kwargs_explicit: the explicitly-specified (higher-precedence) kwargs values.
        These values will take precedence if there is any overlap of keys.
    :param kwargs_defaults: the default (lower-precedence) kwargs values.
    :return: a new dict containing the merged values.
    """
    if kwargs_explicit is None and kwargs_defaults is None:
        return None  # do not return non-None if None was passed

    kwargs_merged = {}
    if kwargs_defaults:
        kwargs_merged.update(kwargs_defaults)
    if kwargs_explicit:
        kwargs_merged.update(kwargs_explicit)
    return kwargs_merged


def stringify(obj):
    """
    Recursively convert a <list> or <dict> object's inner elements to strings.
    """
    # raise NotImplementedError('Broken function!')

    import collections

    if obj is None:
        return None
    if isinstance(obj, str):
        return obj
    if isinstance(obj, unicode):
        return obj.encode('utf-8')

    # if isinstance(obj, dict):
    if isinstance(obj, collections.MutableMapping):
        # it's a dict-like object
        return {stringify(key): stringify(value) for key, value in obj.iteritems()}

    if isinstance(obj, list):
        return [stringify(element) for element in obj]

    if isinstance(obj, set):
        return set(stringify(element) for element in obj)

    if isinstance(obj, collections.Iterable):
        # it's a dict-like object
        return {stringify(key): stringify(value) for key, value in obj.iteritems()}

    return str(obj)
