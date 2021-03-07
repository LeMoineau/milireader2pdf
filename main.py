
import re
import os
import img2pdf  # python3-img2pdf
from pikepdf import _cpphelpers
import urllib.request
import shutil
import json
from PIL import Image

#https://content.milibris.com/access/html5-reader/ffa2a84c-a087-40ab-b4aa-123320933ba8/pages

print("Importation des packages...")

filename = "pierrot"
journal_url = ""

print("Lecture de la clé du journal...")

#On trouve la clé du journal
with open(f"{filename}.html", "r") as f:
    all_keys = re.findall("https://content.milibris.com/access/html5-reader/.{36}", f.read())
    if len(all_keys) > 0:
        journal_url = all_keys[0]
    else:
        print("error")

print(f"Création du dossier container '{filename}'...")

#On créer un dossier pour mettre tous nos composants
try:
    os.mkdir(filename)
except FileExistsError:
    shutil.rmtree(filename)
    os.mkdir(filename)

print("Recupération du fichier 'material.json'...")

#On trouve le fichier material.json
urllib.request.urlretrieve(f"{journal_url}/material.json", f"{filename}/material.json")

print("Création des pages...")

#On récupère l'id des pages
with open(f'{filename}/material.json') as json_file:
    
    data = json.load(json_file)
    compteur_page = 1
    os.mkdir(f"{filename}/tileset")
    os.mkdir(f"{filename}/pages")
    
    for page in data["pages"]:
        
        print(f"Recupération des éléments de la page {compteur_page}...")
        
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
        os.mkdir(f"{filename}/tileset/page-{compteur_page:03}")
        for col in range(0, tile_col_count):
            for row in range(0, tile_row_count):
                
                whereStock = f"{filename}/tileset/page-{compteur_page:03}/tile{col:02}x{row:02}.jpg"
                url = f"{journal_url}/{path}/tile{col:02}x{row:02}.jpeg"
                urllib.request.urlretrieve(url, whereStock)
                
                img = Image.open(whereStock, 'r')
                real_page.paste(img, (tile_width * col, tile_height * row))
        
        #A partir des tiles dl on créer la page
        real_page.save(f'{filename}/pages/page-{compteur_page:03}.jpg')
        
        compteur_page += 1

print(f"Finalisation et création du fichier '{filename}.pdf'...")

#Avec toutes les pages, on créé enfin le pdf final !
with open(f"{filename}/{filename}.pdf", "wb") as f:
    f.write(img2pdf.convert([os.path.join(f"{filename}/pages", i) for i in os.listdir(f"{filename}/pages")]))
        
print(f"fichier {filename}.pdf créé !") 