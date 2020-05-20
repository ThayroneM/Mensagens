from datetime import datetime
import socket
import threading
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
import sys

status = "Livre"
clienteSelecionado = ""

class Principal:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.button1 = tk.Button(self.frame, text = 'New Window', width = 25, command = self.new_window)
        self.button1.pack()
        self.frame.pack()

    def new_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = telaCliente1(self.newWindow)

class telaCliente1:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
        self.quitButton.pack()
        self.frame.pack()

    def close_windows(self):
        self.master.destroy()

root = tk.Tk()
root.title("Server")

text = tk.Text(master=root)
text.pack(expand=True, fill="both")

entry = tk.Entry(master=root)
entry.pack(expand=True, fill="x")

frame = tk.Frame(master=root)
frame.pack()

def buttons():
    for i in "Conectar", "Enviar", "Limpar", "Sair":
        b = tk.Button(master=frame, text=i)
        b.pack(side="left")
        yield b

b1, b2, b3, b4, = buttons()

class Server:
    clients = []

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.s.bind(("", 10001))
        self.s.listen(10)
        now = str(datetime.now())[:-7]

        text.insert("insert", "({}) : Conectado.\n".format(now))
        self.condition()

    def accept(self):
        c, addr = self.s.accept()
        self.clients.append(c)
        data = (c.recv(1024)).decode("UTF-8")

        global status
        global clienteSelecionado

        print(data)

        if data == "Requisicao":
            text.insert("insert", "({}) : {} Conectou.\n".format(str(datetime.now())[:-7], str(data)))
            status = "Ocupado"
        else:
            if status == "Livre":
                #print(status)
                clienteSelecionado = c
                c.sendall(bytes('Livre'.encode("utf-8")))
                #text.insert("insert", "({}) : {} Verificou que você está online.\n".format(str(datetime.now())[:-7], str(data)))
                #self.s.close()

            elif status == "Ocupado":
                print(status)
                c.sendall(bytes(status.encode("utf-8")))
                #text.insert("insert", "({}) : {} Tentou Conectar.\n".format(str(datetime.now())[:-7], str(data)))
                #self.s.close()

    def exibir(self, event):

        print("dados")

    def receive(self):
        for i in self.clients:
            def f():
                data = str(i.recv(1024))[2:-1]
                now = str(datetime.now())[:-7]
                if len(data) == 0:
                    pass
                else:
                    text.insert("insert", "({}) : {}\n".format(now, data))

            t1_2_1 = threading.Thread(target=f)
            t1_2_1.start()

    def condition(self):
        while True:
            t1_1 = threading.Thread(target=self.receive)
            t1_1.daemon = True
            t1_1.start()
            t1_1.join(1)
            t1_2 = threading.Thread(target=self.accept)
            t1_2.daemon = True
            t1_2.start()
            t1_2.join(1)

    def send(self):
        respond = "Server: {}".format(str(entry.get()))
        now = str(datetime.now())[:-7]
        entry.delete("0", "end")

        global clienteSelecionado

        try:
            for i in self.clients:
                if i == clienteSelecionado:
                    i.sendall(bytes(respond.encode("utf-8")))
            text.insert("insert", "({}) : {}\n".format(now, respond))
        except BrokenPipeError:
            text.insert("insert", "({}) : Cliente foi desconectado.\n".format(now))


s1 = Server()


def connect():
    t1 = threading.Thread(target=s1.connect)
    t1.start()


def send():
    t2 = threading.Thread(target=s1.send)
    t2.start()


def clear():
    text.delete("1.0", "end")


def destroy():
    root.destroy()
    exit()


if __name__ == "__main__":
    b1.configure(command=connect)
    b2.configure(command=send)
    b3.configure(command=clear)
    b4.configure(command=destroy)

    t0 = threading.Thread(target=root.mainloop)
    t0.run()