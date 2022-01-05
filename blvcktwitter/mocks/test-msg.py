
from nose.tools import assert_is_not_none

# Local imports...
from mocks.main import get_msgs


def test_request_response():
    # Call the service, which will send a request to the server.
    response = get_msgs()

    # If the request is sent successfully, then I expect a response to be returned.
    assert_is_not_none(response)
