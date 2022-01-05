
from unittest.mock import Mock, patch
from nose.tools import assert_is_none, assert_list_equal, assert_true
from mocks.main import get_msgs, get_uncompleted_msgs


class TestMsgs(object):
    @classmethod
    def setup_class(cls):
        cls.mock_get_patcher = patch('mocks.main.requests.get')
        cls.mock_get = cls.mock_get_patcher.start()

    @classmethod
    def teardown_class(cls):
        cls.mock_get_patcher.stop()

    def test_getting_msgs_when_response_is_ok(self):
        # Configure the mock to return a response with an OK status code.
        self.mock_get.return_value.ok = True

        msg = [{
            'userId': xxx,
            'id': xxx,
            'msgs': 'PvrpleBlvck',
            'completed': False
        }]

        self.mock_get.return_value = Mock()
        self.mock_get.return_value.json.return_value = nsgs

        # Call the service, which will send a request to the server.
        response = get_msgs()

        # If the request is sent successfully, then I expect a response to be returned.
        assert_list_equal(response.json(), msgs)

    def test_getting_msgs_when_response_is_not_ok(self):
        # Configure the mock to not return a response with an OK status code.
        self.mock_get.return_value.ok = False

        # Call the service, which will send a request to the server.
        response = get_msg()

        # If the response contains an error, I should get no msgs.
        assert_is_none(response)


class TestUncompletedMsgs(object):
    @classmethod
    def setup_class(cls):
        cls.mock_get_msgs_patcher = patch('mocks.main.get_msgs')
        cls.mock_get_msgs = cls.mock_get_msgs_patcher.start()

    @classmethod
    def teardown_class(cls):
        cls.mock_get_msgs_patcher.stop()

    def test_getting_uncompleted_todos_when_msgs_is_not_none(self):
        msg1 = {
            'userId': xxx,
            'id': xxx,
            'msg': 'Blvck',
            'completed': False
        }
        msg2 = {
            'userId': yyy,
            'id': yyy,
            'msg': 'Pvrple',
            'completed': True
        }

        # Configure mock to return a response with a JSON-serialized list of msgs.
        self.mock_get_msgs.return_value = Mock()
        self.mock_get_msgs.return_value.json.return_value = [msg1, msg2]

        # Call the main, which will get a list of msgs filtered on completed.
        uncompleted_msgs = get_uncompleted_msgs()

        # Confirm that the mock was called.
        assert_true(self.mock_get_msgs.called)

        # Confirm that the expected filtered list of msgs was returned.
        assert_list_equal(uncompleted_msgs, [msg1])

    def test_getting_uncompleted_msgs_when_msgs_is_none(self):
        # Configure mock to return None.
        self.mock_get_msgs.return_value = None

        # Call the main, which will return an empty list.
        uncompleted_msgs = get_uncompleted_msgs()

        # Confirm that the mock was called.
        assert_true(self.mock_get_todos.called)

        # Confirm that an empty list was returned.
        assert_list_equal(uncompleted_msgs, [])