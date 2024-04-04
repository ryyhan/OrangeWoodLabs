# Imports
import pytest
from unittest.mock import MagicMock
from mqtt import *


# Mock functions
def mock_mqtt_client():
    client = MagicMock()
    return client


def mock_mqtt_message(topic="test/topic", payload=b"Hello"):
    message = MagicMock()
    message.topic = topic
    message.payload = payload
    return message


# Helper function to assert callback calls
def assert_callback_called_with(
    mock_callback, expected_topic=None, expected_payload=None
):
    calls = mock_callback.mock_calls
    assert len(calls) > 0, f"Callback {mock_callback} not called"
    call_args = calls[-1][1]  # Get arguments from the last call
    if expected_topic:
        assert call_args[0].topic == expected_topic
    if expected_payload:
        assert call_args[0].payload == expected_payload


# Test cases

"""
def test_on_mqtt_connect_success():
    # Mock client
    client = mock_mqtt_client()

    # Call the function
    on_mqtt_connect(client, None, None, 0, None)

    # Verify connect and no message call
    assert client.connect.called
    assert not client.on_message.called

def test_on_mqtt_connect_failure():
    # Mock client
    client = mock_mqtt_client()

    # Call the function
    on_mqtt_connect(client, None, None, 1, None)

    # Verify connect and no message call
    assert client.connect.called
    assert not client.on_message.called

def test_on_mqtt_message():
    # Mock client and message
    client = mock_mqtt_client()
    message = mock_mqtt_message()

    # Call the function
    on_mqtt_message(client, None, message)

    # Verify no connect call and message call with arguments
    assert not client.connect.called
    assert_callback_called_with(client.on_message, message.topic, message.payload)
"""


def test_on_mqtt_publish_success():
    # Mock client
    client = mock_mqtt_client()

    # Call the function
    on_mqtt_publish(client, None, 123, 0, None)

    # Verify no connect call and no message call
    assert not client.connect.called
    assert not client.on_message.called


def test_on_mqtt_publish_failure():
    # Mock client
    client = mock_mqtt_client()

    # Call the function
    on_mqtt_publish(client, None, 123, 1, None)

    # Verify no connect call and no message call
    assert not client.connect.called
    assert not client.on_message.called


# Run tests
if __name__ == "__main__":
    pytest.main()
