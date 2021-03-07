
import os
import re
import urllib.request
import json
from PIL import Image

def getkeyurl(directory_name):
    
    """Recupérer la clé d'un journal depuis le fichier html

    parameters:
        directory_name: url du dossier de stockage des fichiers

    returns:
        l'url de base suivant de la clé de 36 caractères du journal 
    """
    
    print("Lecture de la clé du journal...")
    with open(f"{directory_name}.html", "r") as f:
        all_keys = re.findall("https://content.milibris.com/access/html5-reader/.{36}", f.read())
        if len(all_keys) > 0:
            return all_keys[0]
        else:
            exit("La clé n'a pas pu être trouvée")
    
def createlocalmaterial(journal_url, directory_name):
    
    """Créer un fichier material.json dans le dossier de stockage

    parameters:
        journal_url: url du journal avec sa clé
        directory_name: url du dossier de stockage des fichiers
    """
    
    print("Récupération du fichier 'material.json' du journal")
    urllib.request.urlretrieve(f"{journal_url}/material.json", f"{directory_name}/material.json")
    
def generatepages(journal_url, directory_name):
    
    """Genere les pages depuis les informations du fichier material.json

    parameters:
        journal_url: url du journal avec sa clé
        directory_name: url du dossier de stockage des fichiers
    """
    
    print("Création des pages...")
    with open(f'{directory_name}/material.json') as json_file:
    
        #On charge le fichier material.json
        data = json.load(json_file)
        compteur_page = 1
        os.mkdir(f"{directory_name}/tileset")
        os.mkdir(f"{directory_name}/pages")
        
        for page in data["pages"]:
            
            print(f" - page {compteur_page}...")
            
            #On recupère les infos de la page
            content = page["hd"]
            tile_col_count = content["tile_col_count"]
            tile_row_count = content["tile_row_count"]
            tile_height = content["tile_height"]
            tile_width = content["tile_width"]
            width = content["width"]
            height = content["height"]
            path = content["path"]
            
            real_page = Image.new('RGB', (width, height), (255, 255, 255))
            
            #On créer un dossier par page pour dl toutes les parties
            os.mkdir(f"{directory_name}/tileset/page-{compteur_page:03}")
            for col in range(0, tile_col_count):
                for row in range(0, tile_row_count):
                    
                    whereStock = f"{directory_name}/tileset/page-{compteur_page:03}/tile{col:02}x{row:02}.jpg"
                    url = f"{journal_url}/{path}/tile{col:02}x{row:02}.jpeg"
                    urllib.request.urlretrieve(url, whereStock)
                    
                    img = Image.open(whereStock, 'r')
                    real_page.paste(img, (tile_width * col, tile_height * row))
            
            #A partir des tiles dl on créer la page
            real_page.save(f'{directory_name}/pages/page-{compteur_page:03}.jpg')
            
            compteur_page += 1
