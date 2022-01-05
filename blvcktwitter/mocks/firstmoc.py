
from unittest.mock import Mock, patch
from nose.tools import assert_is_not_none

.
from mocks.main import get_msgs


@patch('mocks.main.requests.get')
def test_getting_msgs(mock_get):
    # Configure the mock to return a response with an OK status code.
    mock_get.return_value.ok = True

    # Call the service, which will send a request to the server.
    response = get_msgs()

    # If the request is sent successfully, then I expect a response to be returned.
    assert_is_not_none(response)