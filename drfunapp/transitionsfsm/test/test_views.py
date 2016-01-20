from django.core.urlresolvers import reverse
from nose.tools import eq_, ok_
from rest_framework.test import APITestCase

from ..views import transitionsfsm_root, transitionsfsm_machines_root, transitionsfsm_machines_pk, \
    transitionsfsm_machines_pk_blueprint, transitionsfsm_machines_pk_graph, \
    transitionsfsm_machines_pk_transition


class TestApiRootView(APITestCase):
    """
    Tests the transitionsfsm_root FBV.
    """

    def setUp(self):
        self.url = reverse(transitionsfsm_root)
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
        ok_("'transitionsfsm_root': 'http://testserver/api/v1/transitionsfsm/'" in response_data)
        ok_("'transitionsfsm_machines_root': 'http://testserver/api/v1/transitionsfsm/machines/'" in response_data)
        ok_("'transitionsfsm_machines_pk': 'http://testserver/api/v1/transitionsfsm/machines/matter/'" in response_data)  # noqa
        ok_("'transitionsfsm_machines_pk_blueprint': 'http://testserver/api/v1/transitionsfsm/machines/matter/blueprint/'" in response_data)  # noqa
        ok_("'transitionsfsm_machines_pk_graph': 'http://testserver/api/v1/transitionsfsm/machines/matter/graph/'" in response_data)  # noqa
        ok_("'transitionsfsm_machines_pk_transition': 'http://testserver/api/v1/transitionsfsm/machines/matter/transition/'" in response_data)  # noqa


class TestMachinesRootView(APITestCase):
    """
    Tests the transitionsfsm_machines_root FBV.
    """

    def setUp(self):
        self.url = reverse(transitionsfsm_machines_root)

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


class TestMachinesPKView(APITestCase):
    """
    Tests the transitionsfsm_machines_pk FBV.
    """

    def setUp(self):
        self.url = reverse(transitionsfsm_machines_pk, args=('matter',))

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


class TestMachinesPKBlueprintView(APITestCase):
    """
    Tests the transitionsfsm_machines_pk_blueprint FBV.
    """

    def setUp(self):
        self.url = reverse(transitionsfsm_machines_pk_blueprint, args=('matter',))

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


class TestMachinesPKGraphView(APITestCase):
    """
    Tests the transitionsfsm_machines_pk_graph FBV.
    """

    def setUp(self):
        self.url = reverse(transitionsfsm_machines_pk_graph, args=('matter',))
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


class TestMachinesPKGraphPngView(TestMachinesPKGraphView):
    """
    Tests the transitionsfsm_machines_pk_graph FBV's support for DOT responses.
    """

    def setUp(self):
        self.url = reverse(transitionsfsm_machines_pk_graph, args=('matter', '.png'))
        self.expected_content_type = 'image/png'


class TestMachinesPKGraphJpegView(TestMachinesPKGraphView):
    """
    Tests the transitionsfsm_machines_pk_graph FBV's support for DOT responses.
    """

    def setUp(self):
        self.url = reverse(transitionsfsm_machines_pk_graph, args=('matter', '.jpeg'))
        self.expected_content_type = 'image/jpeg'


class TestMachinesPKGraphDotView(TestMachinesPKGraphView):
    """
    Tests the transitionsfsm_machines_pk_graph FBV's support for DOT responses.
    """

    def setUp(self):
        self.url = reverse(transitionsfsm_machines_pk_graph, args=('matter', '.dot'))
        self.expected_content_type = 'text/plain'


class TestMachinesPKGraphXdot14View(TestMachinesPKGraphView):
    """
    Tests the transitionsfsm_machines_pk_graph FBV's support for DOT responses.
    """

    def setUp(self):
        self.url = reverse(transitionsfsm_machines_pk_graph, args=('matter', '.xdot1.4'))
        self.expected_content_type = 'text/plain'


class TestMachinesPKGraphSvgView(TestMachinesPKGraphView):
    """
    Tests the transitionsfsm_machines_pk_graph FBV's support for DOT responses.
    """

    def setUp(self):
        self.url = reverse(transitionsfsm_machines_pk_graph, args=('matter', '.svg'))
        self.expected_content_type = 'image/svg+xml'


class TestMachinesPKGraphPdfView(TestMachinesPKGraphView):
    """
    Tests the transitionsfsm_machines_pk_graph FBV's support for DOT responses.
    """

    def setUp(self):
        self.url = reverse(transitionsfsm_machines_pk_graph, args=('matter', '.pdf'))
        self.expected_content_type = 'application/pdf'


class TestMachinesPKTransitionView(APITestCase):
    """
    Tests the transitionsfsm_machines_pk_transition FBV.
    """

    def setUp(self):
        self.url = reverse(transitionsfsm_machines_pk_transition, args=('matter',))

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
