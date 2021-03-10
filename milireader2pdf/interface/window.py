
from tkinter import *
import tkinter as tk
from tkinter import filedialog
from milireader2pdf.directory import filemanager
import milireader2pdf.generator as generator
import os

class Window(tk.Frame):

    def __init__(self, frame=tk.Tk()):

        """Constructeur de la fenetre

        parameters:
            frame: nouvelle fenetre tkinter
        """

        super().__init__(frame)
        self.frame = frame
        self.init_frame()

    def init_frame(self):

        """
        Personnalisation rapide de la fenetre
        """

        self.frame.title("Milibris-reader to PDF")
        self.pack()
        self.pack_elements()

    def pack_elements(self):

        """
        Ajout des éléments principaux
        """

        self.info = tk.Label(self)
        self.infovar = StringVar()
        self.info["textvariable"] = self.infovar
        self.infovar.set("aucun fichier selectionné")
        self.info["fg"] = "red"
        self.info.pack(side="top", padx=20, pady=20)

        self.selected_file = "Choisir un fichier"

        self.file_chooser = tk.Button(self)
        self.file_chooser["text"] = self.selected_file
        self.file_chooser["command"] = self.choose_file
        self.file_chooser.pack(side="left", padx=20, pady=20)

        self.test = tk.Button(self, text="Générer", command=self.generate_pdf)
        self.test.pack(side="right", padx=20, pady=20)

    def choose_file(self):

        """
        Fonction de selection d'un fichier
        Stocke dans self.selected_file le chemin complet vers le fichier selectionné
        """

        self.selected_file = filedialog.askopenfilename(initialdir = filemanager.get_root_directory(),
            title = "Select file",
            filetypes = (("html files","*.html"),("all files","*.*")))
        if self.selected_file:
            self.file_chooser["text"] = filemanager.get_only_basename(self.selected_file)
            self.file_chooser.pack()
            self.infovar.set("fichier selectionné")
            self.info["fg"] = "green"
            self.info.pack()
        else:
            self.file_chooser["text"] = "Choisir un fichier"
            self.file_chooser.pack()
            self.infovar.set("aucun fichier selectionné")
            self.info["fg"] = "red"
            self.info.pack()

    def generate_pdf(self):

        """
        Fonction intermédiaire pour appeler la fonction principale de génération
        """

        if (self.selected_file and self.selected_file != "Choisir un fichier"):
            generator.generate(self.selected_file)
