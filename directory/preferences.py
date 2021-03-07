
import json

def getpreferences():
    
    """Lit les préférences du fichier param.txt

    returns:
        un couple (filename, start_step)
    """
    
    print(f"Lecture des préférences du fichier 'param.txt'...")
    with open(f'param.txt') as json_file:
        param = json.load(json_file)
        return (param["filename"], param["start_step"])
