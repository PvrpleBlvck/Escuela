import pytest
import requests

# cassettes/{module_name}/test_single.yaml will be used
@pytest.mark.vcr
def test_single():
    assert requests.get("http://httpbin.org/get").text == '{"get": true}'

# cassettes/{module_name}/example.yaml will be used
@pytest.mark.default_cassette("example.yaml")
@pytest.mark.vcr
def test_default():
    assert requests.get("http://httpbin.org/get").text == '{"get": true}'

# these cassettes will be used in addition to the default one
@pytest.mark.vcr("/path/to/ip.yaml", "/path/to/get.yaml")
def test_multiple():
    assert requests.get("http://httpbin.org/get").text == '{"get": true}'
    assert requests.get("http://httpbin.org/ip").text == '{"ip": true}'