import tkinter as tk
import pytest
from unittest.mock import patch, Mock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.client_gui import ChatClient

@pytest.fixture
def chat_client():
    root = tk.Tk()
    client = ChatClient(root)
    client.connected = True  # Simulate an active connection
    
    yield client
    
    client.stop_event.set()  # Stop the receive_messages thread
    if client.connected:
        client.on_close()  # Ensure connection is closed and resources are cleaned up
    
    root.destroy()  # Destroy the Tkinter root window

def test_send_message(chat_client):
    with patch('src.client_gui.socket.socket', autospec=True) as mock_socket:
        mock_socket_instance = Mock()
        mock_socket.return_value = mock_socket_instance

        chat_client.connected = True
        chat_client.msg_entry.insert(tk.END, "Test message")
        chat_client.send_message(None)

        # Process pending Tkinter events
        chat_client.master.update_idletasks()

        print("Message Entry:", chat_client.msg_entry.get(1.0, tk.END))
        print("Chat Box:", chat_client.chat_box.get(1.0, tk.END))

        mock_socket_instance.send.assert_called_once_with(b'Test message\n')

        assert chat_client.msg_entry.get(1.0, tk.END).strip() == ""
        assert "Vous: Test message" in chat_client.chat_box.get(1.0, tk.END)
