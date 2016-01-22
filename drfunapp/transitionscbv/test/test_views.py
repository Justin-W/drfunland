import random

import sys
from django.core.urlresolvers import reverse
from nose.tools import eq_, ok_
from nose.plugins.attrib import attr
from rest_framework.test import APITestCase

from ..views import transitionscbv_root, transitionscbv_machines_root, \
    transitionscbv_machines_pk, transitionscbv_machines_pk_blueprint, transitionscbv_machines_pk_graph, \
    transitionscbv_machines_pk_snapshot, transitionscbv_machines_pk_transition


def get_machine_snapshot(client, machine_name, verbose=False):
    # url_detail_ = reverse(transitionscbv_machines_pk, args=(machine_name,))
    # snapshot_ = client.get(url_detail_).data['snapshot']
    url_detail_ = reverse(transitionscbv_machines_pk_snapshot, args=(machine_name,))
    snapshot_ = client.get(url_detail_, {'verbose': bool(verbose)}).data
    return snapshot_


class TestApiRootView(APITestCase):
    """
    Tests the transitionscbv_root FBV.
    """

    def setUp(self):
        self.url = reverse(transitionscbv_root)
        self.test_data_in = {'string': 'abc', 'number': 123, 'bool': True, 'list': ['a', 2, 'c']}

    def test_get_request_succeeds(self):
        response = self.client.get(self.url)
        eq_(response.status_code, 200)

    def test_options_request_succeeds(self):
        response = self.client.options(self.url)
        eq_(response.status_code, 200)

    def test_put_request_fails(self):
        response = self.client.put(self.url)
        eq_(response.status_code, 405)

    def test_delete_request_fails(self):
        response = self.client.delete(self.url)
        eq_(response.status_code, 405)

    def test_post_request_with_no_data_fails(self):
        response = self.client.post(self.url, {})
        eq_(response.status_code, 405)

    def test_get_request_with_valid_data_succeeds(self):
        response = self.client.get(self.url, self.test_data_in)
        eq_(response.status_code, 200)

    def test_post_request_with_valid_data_fails(self):
        response = self.client.post(self.url, self.test_data_in)
        eq_(response.status_code, 405)

    def test_get_request_expected_data(self):
        response = self.client.get(self.url, data=self.test_data_in)
        eq_(response.status_code, 200)
        response_data = repr(response.data)
        ok_("'transitionscbv_root', 'http://testserver/api/v1/transitionscbv/'" in response_data)
        ok_("'transitionscbv_machines_root', 'http://testserver/api/v1/transitionscbv/machines/'" in response_data)
        ok_("'transitionscbv_machines_pk', 'http://testserver/api/v1/transitionscbv/machines/matter/'" in response_data)  # noqa
        ok_("'transitionscbv_machines_pk_blueprint', 'http://testserver/api/v1/transitionscbv/machines/matter/blueprint/'" in response_data)  # noqa
        ok_("'transitionscbv_machines_pk_graph', 'http://testserver/api/v1/transitionscbv/machines/matter/graph/'" in response_data)  # noqa
        ok_("'transitionscbv_machines_pk_snapshot', 'http://testserver/api/v1/transitionscbv/machines/matter/snapshot/'" in response_data)  # noqa
        ok_("'transitionscbv_machines_pk_transition', 'http://testserver/api/v1/transitionscbv/machines/matter/transition/'" in response_data)  # noqa


class TestMachinesRootView(APITestCase):
    """
    Tests the transitionscbv_machines_root FBV.
    """

    def setUp(self):
        self.url = reverse(transitionscbv_machines_root)

    def test_get_request_succeeds(self):
        response = self.client.get(self.url)
        eq_(response.status_code, 200)

    def test_options_request_succeeds(self):
        response = self.client.options(self.url)
        eq_(response.status_code, 200)

    def test_put_request_fails(self):
        response = self.client.put(self.url)
        eq_(response.status_code, 405)

    def test_delete_request_fails(self):
        response = self.client.delete(self.url)
        eq_(response.status_code, 405)

    def test_post_request_with_no_data_fails(self):
        response = self.client.post(self.url, {})
        eq_(response.status_code, 400)

    def test_post_request_with_valid_data_succeeds(self):
        # states = ['solid', 'liquid', 'gas', 'plasma']
        # transitions = [
        #     ['melt', 'solid', 'liquid'],
        #     ['evaporate', 'liquid', 'gas'],
        #     ['sublimate', 'solid', 'gas'],
        #     ['ionize', 'gas', 'plasma']
        # ]
        states = ['Unstarted', 'In Progress', 'Completed', 'Cancelled']
        transitions = [
            ['Start', states[0], states[1]],
            ['Complete', states[1], states[2]],
            ['Cancel', states[1], states[3]]
        ]

        self.helper_post_request_with_valid_data_succeeds(states, transitions)

    def test_post_request_with_valid_data_succeeds2(self):
        states = ['Future', 'Current', 'Past', 'Abandoned']
        transitions = [
            ['Begin', states[0], states[1]],
            ['Finish', states[1], states[2]],
            ['Abandon', states[1], states[3]]
        ]

        self.helper_post_request_with_valid_data_succeeds(states, transitions)

    def helper_post_request_with_valid_data_succeeds(self, states, transitions):
        machine_name = 'test{}'.format(random.randint(0, sys.maxint))
        order = states[0:3]  # use the first 3
        initial = states[0]
        data = {'name': machine_name, 'states': states, 'transitions': transitions, 'initial': initial, 'order': order}
        expected = {
            'current': states[0],
            'initial': states[0],
            'states': [states[0], states[1], states[2], states[3]],
            'send_event': False, 'auto_transitions': False, 'ignore_invalid_triggers': False,
            'transitions': [
                {'unless': None, 'dest': states[1], 'after': None, 'source': states[0], 'trigger': transitions[0][0],
                 'conditions': None, 'before': None},
                {'unless': None, 'dest': states[2], 'after': None, 'source': states[1], 'trigger': transitions[1][0],
                 'conditions': None, 'before': None},
                {'unless': None, 'dest': states[3], 'after': None, 'source': states[1], 'trigger': transitions[2][0],
                 'conditions': None, 'before': None},
                {'unless': None, 'dest': states[1], 'after': None, 'source': states[0], 'trigger': 'next_state',
                 'conditions': None, 'before': None},
                {'unless': None, 'dest': states[2], 'after': None, 'source': states[1], 'trigger': 'next_state',
                 'conditions': None, 'before': None},
                {'unless': None, 'dest': states[0], 'after': None, 'source': states[2], 'trigger': 'next_state',
                 'conditions': None, 'before': None}]
        }
        response = self.client.post(self.url, data=data)
        eq_(response.status_code, 200)
        self.assertDictEqual(response.data, expected)
        # get the new object's data from the server, and compare it with the original (intended) values
        snapshot_ = get_machine_snapshot(self.client, machine_name, verbose=True)
        eq_(snapshot_['initial'], initial)
        eq_(snapshot_['current'], initial)
        eq_(snapshot_['states'], states)


class TestMachinesPkView(APITestCase):
    """
    Tests the transitionscbv_machines_pk FBV.
    """

    def setUp(self):
        self.url = reverse(transitionscbv_machines_pk, args=('matter',))

    def test_get_request_succeeds(self):
        response = self.client.get(self.url)
        eq_(response.status_code, 200)

    def test_options_request_succeeds(self):
        response = self.client.options(self.url)
        eq_(response.status_code, 200)

    def test_put_request_fails(self):
        response = self.client.put(self.url)
        eq_(response.status_code, 405)

    def test_delete_request_fails(self):
        response = self.client.delete(self.url)
        eq_(response.status_code, 405)

    def test_post_request_with_no_data_fails(self):
        response = self.client.post(self.url, {})
        eq_(response.status_code, 405)


class TestMachinesPkBlueprintView(APITestCase):
    """
    Tests the transitionscbv_machines_pk_blueprint FBV.
    """

    def setUp(self):
        self.url = reverse(transitionscbv_machines_pk_blueprint, args=('matter',))

    def test_get_request_succeeds(self):
        response = self.client.get(self.url)
        eq_(response.status_code, 200)

    def test_options_request_succeeds(self):
        response = self.client.options(self.url)
        eq_(response.status_code, 200)

    def test_put_request_fails(self):
        response = self.client.put(self.url)
        eq_(response.status_code, 405)

    def test_delete_request_fails(self):
        response = self.client.delete(self.url)
        eq_(response.status_code, 405)

    def test_post_request_with_no_data_fails(self):
        response = self.client.post(self.url, {})
        eq_(response.status_code, 405)


class TestMachinesPkGraphView(APITestCase):
    """
    Tests the transitionscbv_machines_pk_graph FBV.
    """

    def setUp(self):
        self.url = reverse(transitionscbv_machines_pk_graph, args=('matter',))
        self.expected_content_type = 'image/png'

    def test_get_request_succeeds(self):
        response = self.client.get(self.url)
        eq_(response.status_code, 200)
        eq_(response['Content-Type'], self.expected_content_type)

    def test_options_request_succeeds(self):
        response = self.client.options(self.url)
        eq_(response.status_code, 200)

    def test_put_request_fails(self):
        response = self.client.put(self.url)
        eq_(response.status_code, 405)

    def test_delete_request_fails(self):
        response = self.client.delete(self.url)
        eq_(response.status_code, 405)

    def test_post_request_with_no_data_fails(self):
        response = self.client.post(self.url, {})
        eq_(response.status_code, 405)


class TestMachinesPkGraphPngView(TestMachinesPkGraphView):
    """
    Tests the transitionscbv_machines_pk_graph FBV's support for DOT responses.
    """

    def setUp(self):
        self.url = reverse(transitionscbv_machines_pk_graph, args=('matter', '.png'))
        self.expected_content_type = 'image/png'


class TestMachinesPkGraphJpegView(TestMachinesPkGraphView):
    """
    Tests the transitionscbv_machines_pk_graph FBV's support for DOT responses.
    """

    def setUp(self):
        self.url = reverse(transitionscbv_machines_pk_graph, args=('matter', '.jpeg'))
        self.expected_content_type = 'image/jpeg'


class TestMachinesPkGraphDotView(TestMachinesPkGraphView):
    """
    Tests the transitionscbv_machines_pk_graph FBV's support for DOT responses.
    """

    def setUp(self):
        self.url = reverse(transitionscbv_machines_pk_graph, args=('matter', '.dot'))
        self.expected_content_type = 'text/plain'


@attr(skip_travis=1)
class TestMachinesPkGraphXdot14View(TestMachinesPkGraphView):
    """
    Tests the transitionscbv_machines_pk_graph FBV's support for DOT responses.
    """

    def setUp(self):
        self.url = reverse(transitionscbv_machines_pk_graph, args=('matter', '.xdot1.4'))
        self.expected_content_type = 'text/plain'


class TestMachinesPkGraphSvgView(TestMachinesPkGraphView):
    """
    Tests the transitionscbv_machines_pk_graph FBV's support for DOT responses.
    """

    def setUp(self):
        self.url = reverse(transitionscbv_machines_pk_graph, args=('matter', '.svg'))
        self.expected_content_type = 'image/svg+xml'


class TestMachinesPkGraphPdfView(TestMachinesPkGraphView):
    """
    Tests the transitionscbv_machines_pk_graph FBV's support for DOT responses.
    """

    def setUp(self):
        self.url = reverse(transitionscbv_machines_pk_graph, args=('matter', '.pdf'))
        self.expected_content_type = 'application/pdf'


class TestMachinesPkSnapshotView(APITestCase):
    """
    Tests the transitionscbv_machines_pk_snapshot FBV.
    """

    def setUp(self):
        self.machine_name = 'matter'
        self.url = reverse(transitionscbv_machines_pk_snapshot, args=(self.machine_name,))

    def test_get_request_succeeds(self):
        response = self.client.get(self.url)
        eq_(response.status_code, 200)

    def test_options_request_succeeds(self):
        response = self.client.options(self.url)
        eq_(response.status_code, 200)

    def test_put_request_fails(self):
        response = self.client.put(self.url)
        eq_(response.status_code, 405)

    def test_delete_request_fails(self):
        response = self.client.delete(self.url)
        eq_(response.status_code, 405)

    def test_get_request_with_no_data_succeeds(self):
        response = self.client.get(self.url, {})
        eq_(response.status_code, 200)

    def test_get_with_verbose_true_succeeds(self):
        response = self.client.get(self.url, {'verbose': True})
        # expected = {'current': 'liquid', 'send_event': False, 'initial': 'liquid', 'states': ['solid', 'liquid', 'gas', 'plasma'], 'auto_transitions': False, 'ignore_invalid_triggers': False, 'transitions': [{'unless': None, 'dest': 'liquid', 'after': None, 'source': 'solid', 'trigger': 'melt', 'conditions': None, 'before': None}, {'unless': None, 'dest': 'gas', 'after': None, 'source': 'liquid', 'trigger': 'evaporate', 'conditions': None, 'before': None}, {'unless': None, 'dest': 'gas', 'after': None, 'source': 'solid', 'trigger': 'sublimate', 'conditions': None, 'before': None}, {'unless': None, 'dest': 'plasma', 'after': None, 'source': 'gas', 'trigger': 'ionize', 'conditions': None, 'before': None}]}  # noqa
        expected = {
            'current': 'liquid', 'initial': 'liquid',
            'send_event': False, 'auto_transitions': False, 'ignore_invalid_triggers': False,
            'states': ['solid', 'liquid', 'gas', 'plasma'],
            'transitions': [
                {'unless': None, 'dest': 'liquid', 'after': None, 'source': 'solid', 'trigger': 'melt',
                 'conditions': None, 'before': None},
                {'unless': None, 'dest': 'gas', 'after': None, 'source': 'liquid', 'trigger': 'evaporate',
                 'conditions': None, 'before': None},
                {'unless': None, 'dest': 'gas', 'after': None, 'source': 'solid', 'trigger': 'sublimate',
                 'conditions': None, 'before': None},
                {'unless': None, 'dest': 'plasma', 'after': None, 'source': 'gas', 'trigger': 'ionize',
                 'conditions': None, 'before': None}]
        }

        eq_(response.status_code, 200)
        self.assertDictEqual(response.data, expected)

    def test_get_with_verbose_false_succeeds(self):
        response = self.client.get(self.url, {'verbose': False})
        # expected = {'states': ['solid', 'liquid', 'gas', 'plasma'], 'initial': 'liquid', 'current': 'liquid', 'auto_transitions': False, 'ignore_invalid_triggers': False, 'transitions': [{'dest': 'liquid', 'source': 'solid', 'trigger': 'melt'}, {'dest': 'gas', 'source': 'liquid', 'trigger': 'evaporate'}, {'dest': 'gas', 'source': 'solid', 'trigger': 'sublimate'}, {'dest': 'plasma', 'source': 'gas', 'trigger': 'ionize'}]}  # noqa
        expected = {
            'current': 'liquid', 'initial': 'liquid', 'auto_transitions': False, 'ignore_invalid_triggers': False,
            'states': ['solid', 'liquid', 'gas', 'plasma'],
            'transitions': [
                {'dest': 'liquid', 'source': 'solid', 'trigger': 'melt'},
                {'dest': 'gas', 'source': 'liquid', 'trigger': 'evaporate'},
                {'dest': 'gas', 'source': 'solid', 'trigger': 'sublimate'},
                {'dest': 'plasma', 'source': 'gas', 'trigger': 'ionize'}]
        }
        eq_(response.status_code, 200)
        self.assertDictEqual(response.data, expected)


class TestMachinesPkTransitionView(APITestCase):
    """
    Tests the transitionscbv_machines_pk_transition FBV.
    """

    def setUp(self):
        self.machine_name = 'matter'
        self.url = reverse(transitionscbv_machines_pk_transition, args=(self.machine_name,))

    def test_get_request_fails(self):
        response = self.client.get(self.url)
        eq_(response.status_code, 400)

    def test_options_request_succeeds(self):
        response = self.client.options(self.url)
        eq_(response.status_code, 200)

    def test_put_request_fails(self):
        response = self.client.put(self.url)
        eq_(response.status_code, 405)

    def test_delete_request_fails(self):
        response = self.client.delete(self.url)
        eq_(response.status_code, 405)

    def test_get_request_with_no_data_fails(self):
        response = self.client.get(self.url, {})
        eq_(response.status_code, 400)

    def test_post_request_with_no_data_fails(self):
        response = self.client.post(self.url, {})
        eq_(response.status_code, 400)

    # def test_get_request_with_valid_data_succeeds(self):
    #     snapshot_ = get_machine_snapshot(self.client, self.machine_name)
    #     eq_(snapshot_['current'], 'liquid')
    #
    #     response = self.client.get(self.url, {'trigger': 'evaporate', 'destination': 'gas'})
    #     eq_(response.status_code, 200)
    #     # eq_(response.data, '')
    #
    #     snapshot_ = get_machine_snapshot(self.client, self.machine_name)
    #     eq_(snapshot_['current'], 'gas')

    # def test_post_request_with_valid_data_succeeds(self):
    #     snapshot_ = get_machine_snapshot(self.client, self.machine_name)
    #     eq_(snapshot_['current'], 'liquid')
    #
    #     response = self.client.post(self.url, {'trigger': 'evaporate', 'destination': 'gas'})
    #     eq_(response.status_code, 200)
    #     # eq_(response.data, '')
    #
    #     snapshot_ = get_machine_snapshot(self.client, self.machine_name)
    #     eq_(snapshot_['current'], 'gas')
