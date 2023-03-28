import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

host = '127.0.0.1'
port = 9090

class Client:
    
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

        message = tkinter.Tk()
        message.withdraw()

        self.nickname = simpledialog.askstring("NICKNAME", "Please choose a nickname", parent = message)

        self.gui_complete = False
        self.running = True

        gui_thread = threading.Thread(target = self.gui_loop)
        receive_thread = threading.Thread(target = self.receive_loop)

        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.window = tkinter.Tk()
        self.window.configure(bg = "lightgray")

        self.chat_label = tkinter.Label(self.window, text = "Chat", bg = "lightgray")
        self.chat_label.config(font = ("arial", 12))
        self.chat_label.pack(padx = 20, pady = 5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.window)
        self.text_area.pack(padx = 20, pady = 5)
        self.text_area.config(state='disabled')

        self.message_label = tkinter.Label(self.window, text = "Message", bg = "lightgray")
        self.message_label.config(font = ("arial", 12))
        self.message_label.pack(padx = 20, pady = 5)

        self.input_area = tkinter.Text(self.window, height = 3)
        self.input_area.pack(padx = 20, pady = 5)

        self.send_button = tkinter.Button(self.window, text = "Send", command = self.write)
        self.send_button.config(font = ("arial", 12))
        self.send_button.pack(padx = 20, pady = 5)

        self.gui_complete = True
        self.window.protocol("WM_DELETE_WINDOW", self.stop)
        self.window.mainloop()

    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        self.socket.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.window.destroy()
        self.socket.close()
        exit(0)

    def receive_loop(self):
        while self.running:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if message == "NICKNAME":
                    self.socket.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_complete:
                        self.text_area.config(state = 'normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state = 'disabled')

            except ConnectionAbortedError:
                break

            except:
                print("Error occured...")
                self.socket.close()
                break

client = Client(host, port)