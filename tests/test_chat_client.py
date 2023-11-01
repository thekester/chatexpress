import pytest
from unittest.mock import Mock, patch, create_autospec
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.ChatClient import ChatClient
import socket

@pytest.fixture
def chat_client():
    client = ChatClient()
    client.gui = Mock()
    yield client

def test_connect_to_server(chat_client):
    # Création d'une spécification automatique pour un socket
    spec_socket = create_autospec(socket.socket, instance=True)
    
    with patch('socket.socket', return_value=spec_socket):
        chat_client.connected = False  # S'assurer que le client n'est pas déjà connecté
        chat_client.gui = Mock()  # S'assurer que la GUI est définie
        print("Avant connect_to_server")
        chat_client.connect_to_server()
        print("Après connect_to_server")
        print("Socket utilisé pour la connexion:", chat_client.client_socket)
        print("Socket mocké:", spec_socket)
        spec_socket.connect.assert_called_with(('localhost', 5555))



def test_send_message(chat_client):
    chat_client.connected = True
    chat_client.gui.get_message.return_value = "Test message"
    
    # Création d'une spécification automatique pour un socket
    spec_socket = create_autospec(socket.socket, instance=True)
    
    with patch('socket.socket', return_value=spec_socket):
        chat_client.client_socket = spec_socket  # Utilisation du socket mocké
        chat_client.send_message(None)
        chat_client.gui.clear_message.assert_called_once()
        chat_client.gui.update_chat_box.assert_called_with("Vous: Test message\n")
