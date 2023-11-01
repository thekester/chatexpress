import tkinter as tk
from tkinter import scrolledtext

class ChatGUI:
    """
    Interface graphique pour l'application de chat.

    Cette classe crée et gère les widgets de l'interface utilisateur pour
    l'application de chat, y compris la boîte de chat, la zone de saisie
    du message et les boutons.

    :param master: La fenêtre principale de l'application Tkinter.
    :param on_send_message: Fonction à appeler lorsque l'utilisateur envoie un message.
    :param on_connect: Fonction à appeler pour établir la connexion au serveur de chat.
    :param on_close: Fonction à appeler lorsque la fenêtre de l'application est fermée.
    """
    def __init__(self, master, on_send_message, on_connect, on_close):
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", on_close)
        master.title("Chat en Temps Réel")
        
        self.status_label = tk.Label(master, text="Déconnecté", fg="red")
        self.status_label.pack(pady=5)

        self.chat_box = scrolledtext.ScrolledText(master, state='disabled', height=15)
        self.chat_box.pack(padx=20, pady=5, expand=True, fill='both')
        
        self.msg_entry = tk.Text(master, height=3)
        self.msg_entry.pack(padx=20, pady=5, fill='x')
        self.msg_entry.bind('<Control-Return>', on_send_message)

        self.connect_button = tk.Button(master, text="Connecter", command=on_connect)
        self.connect_button.pack(pady=5)

    def update_chat_box(self, message):
        """
        Ajoute un message à la boîte de chat.

        :param message: Le message à ajouter à la boîte de chat.
        """
        self.chat_box.configure(state='normal')
        self.chat_box.insert(tk.END, message)
        self.chat_box.configure(state='disabled')
        self.chat_box.yview(tk.END)

    def update_status(self, text, color):
        """
        Met à jour le statut de la connexion.

        :param text: Le texte à afficher comme statut.
        :param color: La couleur du texte du statut.
        """
        self.status_label.config(text=text, fg=color)

    def get_message(self):
        """
        Récupère le message saisi par l'utilisateur dans la zone de saisie.

        :return: Le message saisi par l'utilisateur.
        :rtype: str
        """
        return self.msg_entry.get(1.0, tk.END).strip()

    def clear_message(self):
        """
        Efface le message actuellement saisi dans la zone de saisie.
        """
        self.msg_entry.delete(1.0, tk.END)
