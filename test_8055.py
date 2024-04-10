import json
from unittest.mock import patch, MagicMock
from port_8055 import *

def test_connect_to_controller(mocker):
  """Tests the connect_to_controller function with mocks"""
  # Mock the socket creation and connection
  mock_socket = MagicMock()
  mocker.patch('socket.socket').return_value = mock_socket
  
  # Test successful connection
  success, sock = connect_to_controller("127.0.0.1")
  assert success is True
  assert sock == mock_socket

  # Test with pre-defined exception (modify as needed)
  mock_socket.connect.side_effect = Exception("Connection error")
  success, sock = connect_to_controller("another_ip")
  assert success is False
  assert sock is None

def test_disconnect_from_controller(mocker):
  """Tests proper disconnection with mocked socket"""
  mock_sock = MagicMock()
  disconnect_from_controller(mock_sock)
  mock_sock.close.assert_called_once()

@patch('socket.socket')
def test_send_command_success(mock_socket):
  """Tests send_command with mocked socket and successful response"""
  # Mock socket behavior (modify response data as needed)
  mock_socket.return_value.sendall.side_effect = None
  mock_socket.return_value.recv.return_value = b'{"result": "success", "jsonrpc": "2.0", "id": 1}'
  success, result, _ = send_command(mock_socket.return_value, "test_cmd")
  assert success is True
  assert result == "success"

@patch('socket.socket')
def test_send_command_failure(mock_socket):
  """Tests send_command with mocked socket and error response"""
  # Mock socket behavior (modify error data as needed)
  mock_socket.return_value.sendall.side_effect = None
  mock_socket.return_value.recv.return_value = b'{"error": {"message": "Command failed"}, "jsonrpc": "2.0", "id": 1}'
  success, result, _ = send_command(mock_socket.return_value, "test_cmd")
  assert success is False
  assert result["message"] == "Command failed"

@patch('socket.socket')
def test_send_command_exception(mock_socket):
  """Tests send_command with mocked socket and exception"""
  # Mock socket behavior (modify exception type as needed)
  mock_socket.return_value.sendall.side_effect = Exception("Socket error")
  success, result, _ = send_command(mock_socket.return_value, "test_cmd")
  assert success is False
  assert result is None
