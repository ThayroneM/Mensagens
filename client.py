from datetime import datetime
import socket
import threading
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


root = tk.Tk()
root.title("Client")

text = tk.Text(master=root)
text.pack(expand=True, fill="both")

entry = tk.Entry(master=root)
entry.pack(expand=True, fill="x")

frame = tk.Frame(master=root)
frame.pack()


def buttons():
    for i in "Conectar", "Criar Usuário", "Limpar", "Sair":
        b = tk.Button(master=frame, text=i)
        b.pack(side="left")
        yield b

b1, b2, b3, b4, = buttons()

class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nickname = None

    def connect(self):
        now = str(datetime.now())[:-7]
        if self.nickname is not None:
            try:
                self.s.connect(("127.0.0.1", 10001))
                text.insert("insert", "({}) : Conectado.\n".format(now))
                b1.destroy()

                self.s.sendall(bytes("{}".format(self.nickname).encode("utf-8")))
                self.receive()
            except ConnectionRefusedError:
                text.insert("insert", "({}) : O server não está online.\n".format(now))
        else:
            text.insert("insert", "({}) : Você deve criar um nome de usuário.\n".format(now))

    def receive(self):
        while True:
            data = str(self.s.recv(1024))[2:-1]
            now = str(datetime.now())[:-7]
            if len(data) == 0:
                pass
            else:
                text.insert("insert", "({}) : {}\n".format(now, data))

    def do_nothing(self):
        pass

    def create_nickname(self):
        b2.configure(command=self.do_nothing)
        _frame = tk.Frame(master=root)
        _frame.pack()
        new_entry = tk.Entry(master=_frame)
        new_entry.grid(row=0, column=0)
        new_button = tk.Button(master=_frame, text="Aceitar")
        new_button.grid(row=1, column=0)

        def nickname_command():
            now = str(datetime.now())[:-7]
            if new_entry.get() == "":
                text.insert("insert", "({}) : Você deve digitar o nome do usuário.\n".format(now))
            else:
                self.nickname = new_entry.get()
                _frame.destroy()
                text.insert("insert", "({}) : Seu nome mudou para: '{}'\n".format(now, self.nickname))
                b2.configure(command=c1.create_nickname)

        new_button.configure(command=nickname_command)

    def send(self):
        respond = "{}: {}".format(self.nickname, str(entry.get()))
        now = str(datetime.now())[:-7]
        entry.delete("0", "end")
        try:
            self.s.sendall(bytes(respond.encode("utf-8")))
            text.insert("insert", "({}) : {}\n".format(now, respond))
        except BrokenPipeError:
            text.insert("insert", "({}) : Server foi desconectado.\n".format(now))
            self.s.close()


c1 = Client()


def connect():
    t1 = threading.Thread(target=c1.connect)
    t1.start()


def send(self):
    t2 = threading.Thread(target=c1.send)
    t2.start()


def clear():
    text.delete("1.0", "end")


def destroy():
    root.destroy()


if __name__ == "__main__":
    b1.configure(command=connect)
    b2.configure(command=c1.create_nickname)
    #b3.configure(command=send)
    b3.configure(command=clear)
    b4.configure(command=destroy)

    entry.bind("<Return>", send)

    t0 = threading.Thread(target=root.mainloop)
    t0.run()