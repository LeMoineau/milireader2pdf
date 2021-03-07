
import os
import shutil
import img2pdf
from pikepdf import _cpphelpers

def newdirectory(directory_url):
    
    """Créer un nouveau dossier en supprimant tout son contenu si était déjà existant

    parameters:
        directory_url: url du dossier de stockage
    """
    
    print(f"Création du dossier '{directory_url}'...")
    try:
        os.mkdir(directory_url)
    except FileExistsError:
        shutil.rmtree(directory_url)
        os.mkdir(directory_url)

def generatepdf(directory_name):
    
    """Genere un fichier pdf depuis les pages .jpeg contenu dans le dossier de stockage

    parameters:
        directory_name: url du dossier de stockage
    """
    
    print(f"Finalisation et création du fichier '{directory_name}.pdf'...")
    with open(f"{directory_name}.pdf", "wb") as f:
        f.write(img2pdf.convert([os.path.join(f"{directory_name}/pages", i) for i in os.listdir(f"{directory_name}/pages")]))
