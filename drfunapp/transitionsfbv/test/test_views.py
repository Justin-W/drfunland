import random

import sys
from django.core.urlresolvers import reverse
from nose.tools import eq_, ok_
from rest_framework.test import APITestCase
# from datadiff import diff
# from datadiff.tools import assert_equal as dd_assert_equal

from ..views import transitionsfbv_root, transitionsfbv_machines_root, \
    transitionsfbv_machines_pk, transitionsfbv_machines_pk_blueprint, transitionsfbv_machines_pk_graph, \
    transitionsfbv_machines_pk_transition


def get_machine_snapshot(client, machine_name):
    url_detail_ = reverse(transitionsfbv_machines_pk, args=(machine_name,))
    snapshot_ = client.get(url_detail_).data['snapshot']
    return snapshot_


class TestApiRootView(APITestCase):
    """
    Tests the transitionsfbv_root FBV.
    """

    def setUp(self):
        self.url = reverse(transitionsfbv_root)
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
        ok_("'transitionsfbv_root': 'http://testserver/api/v1/transitionsfbv/'" in response_data)
        ok_("'transitionsfbv_machines_root': 'http://testserver/api/v1/transitionsfbv/machines/'" in response_data)
        ok_("'transitionsfbv_machines_pk': 'http://testserver/api/v1/transitionsfbv/machines/matter/'" in response_data)  # noqa
        ok_("'transitionsfbv_machines_pk_blueprint': 'http://testserver/api/v1/transitionsfbv/machines/matter/blueprint/'" in response_data)  # noqa
        ok_("'transitionsfbv_machines_pk_graph': 'http://testserver/api/v1/transitionsfbv/machines/matter/graph/'" in response_data)  # noqa
        ok_("'transitionsfbv_machines_pk_transition': 'http://testserver/api/v1/transitionsfbv/machines/matter/transition/'" in response_data)  # noqa


class TestMachinesRootView(APITestCase):
    """
    Tests the transitionsfbv_machines_root FBV.
    """

    def setUp(self):
        self.url = reverse(transitionsfbv_machines_root)

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
            'send_event': False, 'auto_transitions': True, 'ignore_invalid_triggers': None,
            'transitions': [
                {'unless': None, 'dest': states[1], 'after': None, 'source': states[0], 'trigger': transitions[0][0],
                 'conditions': None, 'before': None},
                {'unless': None, 'dest': states[2], 'after': None, 'source': states[1], 'trigger': transitions[0][1],
                 'conditions': None, 'before': None},
                {'unless': None, 'dest': states[3], 'after': None, 'source': states[1], 'trigger': transitions[0][2],
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
        eq_(sorted(dict(response.data)), sorted(expected))
        snapshot_ = get_machine_snapshot(self.client, machine_name)
        eq_(snapshot_['current'], initial)
        eq_(snapshot_['states'], states)


class TestMachinesPkView(APITestCase):
    """
    Tests the transitionsfbv_machines_pk FBV.
    """

    def setUp(self):
        self.url = reverse(transitionsfbv_machines_pk, args=('matter',))

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
    Tests the transitionsfbv_machines_pk_blueprint FBV.
    """

    def setUp(self):
        self.url = reverse(transitionsfbv_machines_pk_blueprint, args=('matter',))

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
    Tests the transitionsfbv_machines_pk_graph FBV.
    """

    def setUp(self):
        self.url = reverse(transitionsfbv_machines_pk_graph, args=('matter',))
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
    Tests the transitionsfbv_machines_pk_graph FBV's support for DOT responses.
    """

    def setUp(self):
        self.url = reverse(transitionsfbv_machines_pk_graph, args=('matter', '.png'))
        self.expected_content_type = 'image/png'


class TestMachinesPkGraphJpegView(TestMachinesPkGraphView):
    """
    Tests the transitionsfbv_machines_pk_graph FBV's support for DOT responses.
    """

    def setUp(self):
        self.url = reverse(transitionsfbv_machines_pk_graph, args=('matter', '.jpeg'))
        self.expected_content_type = 'image/jpeg'


class TestMachinesPkGraphDotView(TestMachinesPkGraphView):
    """
    Tests the transitionsfbv_machines_pk_graph FBV's support for DOT responses.
    """

    def setUp(self):
        self.url = reverse(transitionsfbv_machines_pk_graph, args=('matter', '.dot'))
        self.expected_content_type = 'text/plain'


class TestMachinesPkGraphXdot14View(TestMachinesPkGraphView):
    """
    Tests the transitionsfbv_machines_pk_graph FBV's support for DOT responses.
    """

    def setUp(self):
        self.url = reverse(transitionsfbv_machines_pk_graph, args=('matter', '.xdot1.4'))
        self.expected_content_type = 'text/plain'


class TestMachinesPkGraphSvgView(TestMachinesPkGraphView):
    """
    Tests the transitionsfbv_machines_pk_graph FBV's support for DOT responses.
    """

    def setUp(self):
        self.url = reverse(transitionsfbv_machines_pk_graph, args=('matter', '.svg'))
        self.expected_content_type = 'image/svg+xml'


class TestMachinesPkGraphPdfView(TestMachinesPkGraphView):
    """
    Tests the transitionsfbv_machines_pk_graph FBV's support for DOT responses.
    """

    def setUp(self):
        self.url = reverse(transitionsfbv_machines_pk_graph, args=('matter', '.pdf'))
        self.expected_content_type = 'application/pdf'


class TestMachinesPkTransitionView(APITestCase):
    """
    Tests the transitionsfbv_machines_pk_transition FBV.
    """

    def setUp(self):
        self.machine_name = 'matter'
        self.url = reverse(transitionsfbv_machines_pk_transition, args=(self.machine_name,))

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

    def test_post_request_with_valid_data_succeeds(self):
        snapshot_ = get_machine_snapshot(self.client, self.machine_name)
        eq_(snapshot_['current'], 'liquid')

        response = self.client.post(self.url, {'trigger': 'evaporate', 'destination': 'gas'})
        eq_(response.status_code, 200)
        # eq_(response.data, '')

        snapshot_ = get_machine_snapshot(self.client, self.machine_name)
        eq_(snapshot_['current'], 'gas')