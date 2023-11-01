import socket
import threading

class ChatClient:
    """
    Client pour l'application de chat.

    Cette classe gère la connexion au serveur de chat, l'envoi et la réception de messages,
    et interagit avec l'interface utilisateur pour afficher les messages et les statuts.

    :ivar gui: L'interface graphique associée à ce client.
    :ivar client_socket: Le socket utilisé pour la connexion au serveur.
    :ivar connected: Un booléen indiquant si le client est actuellement connecté.
    :ivar stop_event: Un événement utilisé pour arrêter le thread de réception des messages.
    """
    def __init__(self):
        """
        Initialise le client de chat.
        """
        self.gui = None
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.stop_event = threading.Event()

    def connect_to_server(self):
        """
        Connecte le client au serveur de chat.

        Si le client est déjà connecté, affiche un message dans la boîte de chat.
        Sinon, tente de se connecter au serveur et lance un thread pour recevoir les messages.
        """
        if self.gui is None:
            print("La GUI n'est pas encore définie.")
            return

        if not self.connected:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.client_socket.connect(('localhost', 5555))
                self.connected = True
                self.gui.update_status("Connecté", "green")
                threading.Thread(target=self.receive_messages).start()
            except socket.error as e:
                print("Erreur de connexion:", e)
                self.gui.update_chat_box("Impossible de se connecter au serveur.\n")
        else:
            self.gui.update_chat_box("Déjà connecté au serveur.\n")

    def send_message(self, event):
        """
        Envoie un message au serveur de chat.

        :param event: L'événement qui a déclenché cet appel (peut être None).
        """
        if not self.connected:
            print("Not connected")
            return
        message = self.gui.get_message()
        if message:
            try:
                self.client_socket.send((message + "\n").encode('utf-8'))
                self.gui.clear_message()
                self.gui.update_chat_box("Vous: " + message + "\n")
            except Exception as e:
                print("Failed to send message:", str(e))
        else:
            print("Message is empty")

    def receive_messages(self):
        """
        Reçoit les messages du serveur de chat.

        Ce méthode est destinée à être exécutée dans un thread séparé.
        Elle écoute les messages du serveur et les affiche dans la boîte de chat.
        """
        while self.connected and not self.stop_event.is_set():
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if not message:
                    self.connected = False
                    self.gui.update_status("Déconnecté", "red")
                    break
                self.gui.update_chat_box("Serveur: " + message + "\n")
            except ConnectionResetError:
                self.connected = False
                self.gui.update_status("Déconnecté", "red")
                self.gui.update_chat_box("La connexion a été réinitialisée par le serveur.\n")
                break

    def on_close(self):
        """
        Gère la fermeture de l'application.

        Ferme la connexion au serveur si elle est ouverte, et détruit la fenêtre de l'application.
        """
        if self.connected:
            self.stop_event.set()
            self.client_socket.close()
        self.gui.master.destroy()

    def set_gui(self, gui):
        """
        Associe une interface graphique à ce client.

        :param gui: L'instance de ChatGUI à associer à ce client.
        """
        self.gui = gui