from tkinter import*
import autoCH
import webbrowser

delEnabled = "NÃO"

class Application:
    def __init__(self, master=None):
        self.fontePadrao = ("League Spartan Bold", "10")
        self.widget1 = Frame(master)
        self.widget1["padx"] = 20
        self.widget1["pady"] = 20
        self.widget1.pack()
        self.segundoContainer = Frame(master)
        self.segundoContainer["padx"] = 30
        self.segundoContainer.pack()
        
        #Título
        self.titulo = Label(self.widget1, text="Hora de Sede", font=("League Spartan Bold", "20"))
        self.titulo.pack()
        
        # Botão RODAR
        self.prog = Button(self.widget1, text="ENVIAR DADOS", font=self.fontePadrao)
        self.prog.bind("<Button-1>", self.pg)
        self.prog.pack()
        
        # Outros Botões
        self.button1 = Button(self.widget1, text="Github", command=lambda: webbrowser.open('https://github.com/optimusjr/autoCH'), font=self.fontePadrao)
        self.button1.pack(side=LEFT)
        self.button2 = Button(self.widget1, text="Planilha", command=lambda: webbrowser.open("https://docs.google.com/spreadsheets/d/" + autoCH.SPREADSHEET_ID), font=self.fontePadrao)
        self.button2.pack(side=LEFT)
        self.button3 = Button(self.widget1,text= "Deletar EMAILs", font=self.fontePadrao)
        self.button3.bind("<Button-1>", self.deletar)
        self.button3.pack(side=LEFT)
    
    def deletar(self, event):
        autoCH.delete_messages(autoCH.gmail_authenticate(), "Hora de entrada")
            
    def pg(self, event):
        dados = autoCH.prog()
        if len(dados) == 0:
            self.texto1 = Label(self.segundoContainer, text="Nenhum dado foi enviado para a planilha", font=self.fontePadrao)
            self.texto1.pack()
        else:
            self.texto1 = Label(self.segundoContainer, text="Dados enviados para a planilha: ", font=self.fontePadrao)
            self.texto1.pack()
            for i in range(len(dados)):
                self.saida = Label(self.segundoContainer, text=dados[i], font=self.fontePadrao)
                self.saida.pack()

def prog():     
    root = Tk()
    root.title("Hora de Sede")
    Application(root)
    root.mainloop()
