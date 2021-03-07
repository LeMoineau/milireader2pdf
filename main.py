
from milireader2pdf.data import journal
from milireader2pdf.directory import filemanager
from milireader2pdf.directory import preferences

def main():

    """
        Let's generate it !
    """

    (filename, start_step) = preferences.getpreferences()

    if (start_step <= 0):
        journal_url = journal.getkeyurl(filename)
        filemanager.newdirectory(filename)
        journal.createlocalmaterial(journal_url, filename)
        journal.generatepages(journal_url, filename)
        filemanager.generatepdf(filename)
    elif (start_step > 0):
        filemanager.generatepdf(filename)
            
    print(f"fichier {filename}.pdf créé !") 

if __name__ == "__main__":
    main()