
from milireader2pdf.data import journal
from milireader2pdf.directory import filemanager
from milireader2pdf.directory import preferences

def generate(filename):

    """Fonctionnement global de la génération du fichier pdf à partir du fichier html

    parameters:
        filename: chemin complet avec extension du fichier html
    """

    (namefile, start_step) = preferences.get_preferences()
    directory_name = filemanager.get_filename_without_ext(filemanager.get_only_basename(filename))

    if (start_step <= 0):
        journal_url = journal.get_key_url(filename)
        filemanager.new_directory(directory_name)
        journal.create_local_material(journal_url, directory_name)
        journal.generate_pages(journal_url, directory_name)
        filemanager.generate_pdf(directory_name)
    elif (start_step > 0):
        filemanager.generate_pdf(directory_name)

    print(f"fichier {directory_name}.pdf créé !")
