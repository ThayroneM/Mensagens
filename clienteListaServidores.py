from datetime import datetime
import socket
import threading
import time
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

encerrarLoop = False

root = tk.Tk()
root.title("Funcionarios")
root.geometry("400x400")

b1 = tk.Button(master=root, text='Iniciar Conversa')
b2 = tk.Button(master=root, text='Iniciar Conversa')
b3 = tk.Button(master=root, text='Iniciar Conversa')
b4 = tk.Button(master=root, text='Iniciar Conversa')
b5 = tk.Button(master=root, text='Iniciar Conversa')
b6 = tk.Button(master=root, text='Iniciar Conversa')

l1 = tk.Label(master=root)
l2 = tk.Label(master=root)
l3 = tk.Label(master=root)
l4 = tk.Label(master=root)
l5 = tk.Label(master=root)
l6 = tk.Label(master=root)

b = [b1, b2, b3, b4, b5, b6]
l = [l1, l2, l3, l4, l5, l6]

iconVermelho = tk.PhotoImage(file="vermelhop.png")
iconVerde = tk.PhotoImage(file="verdep.png")
iconAmarelo = tk.PhotoImage(file="amarelop.png")

def all_children(window):
    _list = window.winfo_children()

    for item in _list:
        if item.winfo_children():
            _list.extend(item.winfo_children())

    return _list

def iniciarConversa(porta, label):

    global encerrarLoop
    encerrarLoop = True

    label.configure(image=iconAmarelo)
    #button.grid_forget()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", porta))

    s.sendall(bytes("Requisicao".encode("utf-8")))
    #data = ((s.recv(1024)).decode('UTF-8'))

#def configurarBotao(contagem, porta, label):

    #b[contagem].configure(command= lambda: iniciarConversa(porta, label, b[contagem]))
    #b[contagem].grid(row=contagem, column=2)

def nada():
    pass

def executarLoop(root):

    portas = [10001, 10002, 10003, 10005, 10011, 10077]
    nomes = ['Alexandre', 'Cilleni', 'José', 'Thayrone', 'Elisa', 'Lairton']

    while True:
        if encerrarLoop == False:
            contagem = 0
            print("Verificando...")
            # s.settimeout(2)

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # s.setdefaulttimeout(float(100))

            for porta in portas:
                # print(porta)
                #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    s.connect(("127.0.0.1", porta))
                    label = tk.Label(master=root, text=nomes[contagem])
                    label.grid(row=contagem, column=0)

                    s.sendall(bytes("Cliente".encode("utf-8")))
                    while True:
                        data = ((s.recv(1024)).decode('UTF-8'))
                        print(data)
                        if data.strip() == "Livre":
                            l[contagem] = tk.Label(master=root, image=iconVerde)
                            l[contagem].grid(row=contagem, column=1)

                            label.bind("<Button-1>", lambda: iniciarConversa(porta, l[contagem]))
                            #label.configure(command= lambda: iniciarConversa(porta, l[contagem]))
                            #tButton = threading.Thread(target=configurarBotao, args=(contagem, porta, l[contagem]))
                            #tButton.start()

                            break
                        elif data.strip() == "Ocupado":
                            l[contagem] = tk.Label(master=root, image=iconAmarelo)
                            l[contagem].grid(row=contagem, column=1)

                            label.bind("<Button-1>", nada())

                            #b[contagem].grid_forget()
                            break
                        else:
                            break
                    # threading.Thread(target=receber, args=(s,))

                except Exception as erro:
                    label = tk.Label(master=root, text=nomes[contagem])
                    label.grid(row=contagem, column=0)

                    l[contagem] = tk.Label(master=root, image=iconVermelho)
                    l[contagem].grid(row=contagem, column=1)

                    label.bind("<Button-1>", nada())

                    print("Error Connect: ", erro)

                # s.close()
                contagem = contagem + 1
                # print(contagem)
            time.sleep(1)
def receber(s):
    print("receber")
    print(str(s.recv(1024)))

t0 = threading.Thread(target=executarLoop, args=(root,))
t0.start()

if __name__ == "__main__":
    t1 = threading.Thread(target=root.mainloop())
    t1.start()







