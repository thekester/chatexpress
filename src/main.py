import tkinter as tk
from ChatGUI import ChatGUI
from ChatClient import ChatClient

if __name__ == "__main__":
    """
    Script principal pour démarrer l'application de chat.

    Ce script crée une instance de Tkinter, initialise le client et l'interface utilisateur,
    et démarre la boucle principale de Tkinter.
    """

    # Création de la fenêtre principale de Tkinter
    root = tk.Tk()

    # Initialisation du client de chat
    client = ChatClient()

    # Initialisation de l'interface utilisateur et association avec le client
    gui = ChatGUI(root, client.send_message, client.connect_to_server, client.on_close)
    client.set_gui(gui)

    # Connexion au serveur de chat
    client.connect_to_server()

    # Démarrage de la boucle principale de Tkinter
    root.mainloop()
