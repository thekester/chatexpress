import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.stop_event = threading.Event()
        master.title("Chat en Temps Réel")
        
        self.status_label = tk.Label(master, text="Déconnecté", fg="red")
        self.status_label.pack(pady=5)

        self.chat_box = scrolledtext.ScrolledText(master, state='disabled', height=15)
        self.chat_box.pack(padx=20, pady=5, expand=True, fill='both')
        
        self.msg_entry = tk.Text(master, height=3)
        self.msg_entry.pack(padx=20, pady=5, fill='x')
        self.msg_entry.bind('<Control-Return>', self.send_message)

        self.connect_button = tk.Button(master, text="Connecter", command=self.connect_to_server)
        self.connect_button.pack(pady=5)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.connect_to_server()

    def connect_to_server(self):
        if not self.connected:
            try:
                self.client_socket.connect(('localhost', 5555))
                self.connected = True
                self.status_label.config(text="Connecté", fg="green")
                threading.Thread(target=self.receive_messages).start()
            except socket.error as e:
                print("Erreur de connexion:", e)
                self.update_chat_box("Impossible de se connecter au serveur.\n")
        else:
            self.update_chat_box("Déjà connecté au serveur.\n")

    def send_message(self, event):
        print("send_message is called")
        if not self.connected:
            print("Not connected")
            return
        message = self.msg_entry.get(1.0, tk.END).strip()
        print(f"Message: {message}")
        if message:
            print("Sending message:", message)
            try:
                self.client_socket.send((message + "\n").encode('utf-8'))
                self.msg_entry.delete(1.0, tk.END)
                self.update_chat_box("Vous: " + message + "\n")
            except Exception as e:
                print("Failed to send message:", str(e))
        else:
            print("Message is empty")



    def receive_messages(self):
        while self.connected and not self.stop_event.is_set():
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if not message:
                    self.connected = False
                    if threading.current_thread() == threading.main_thread() and self.master.winfo_exists():
                        self.update_status("Déconnecté", "red")
                    break
                if threading.current_thread() == threading.main_thread() and self.master.winfo_exists():
                    self.update_chat_box("Serveur: " + message + "\n")
            except ConnectionResetError:
                self.connected = False
                if threading.current_thread() == threading.main_thread() and self.master.winfo_exists():
                    self.update_status("Déconnecté", "red")
                    self.update_chat_box("La connexion a été réinitialisée par le serveur.\n")
                break


    def update_chat_box(self, message):
        self.chat_box.configure(state='normal')
        self.chat_box.insert(tk.END, message)
        self.chat_box.configure(state='disabled')
        self.chat_box.yview(tk.END)

    def update_status(self, text, color):
        self.status_label.config(text=text, fg=color)

    def on_close(self):
            if self.connected:
                self.stop_event.set()
                self.client_socket.close()
            self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
