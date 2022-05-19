import sys
import time
import csv
import Exceptions

ENDLINE = "_" * 80
open("notebook_data.csv", "a")

def get_last_id():
    """Get the ID of the last note added to the table Notebook.

    :param: None
    :return None
    """
    notebook_file = open("notebook_data.csv", "r")
    reader = csv.reader(notebook_file)

    return sum(1 for row in reader) + 1

class Note:
    """Class helps you create a single note."""
    def __init__(self, text, tag, day, id):
        """Inits NOTE.

        :param text (str): the text of the note.
        :param tag (str): the tag of the note.
        :param day (str): the day create the note.
        :param id (int):  the ID of the note.
        """
        self.text = text
        self.tag = tag
        self.day = day
        self.id = id

class Notebook:
    """Class contains all the notes.

    Create a menu of options for queries with notebook.
    """
    def __init__(self):
        """Inits notebook.

        :param last_id (int): the ID for the newly added note.
        :param options (list): the menu of the notebook.
        :param ID (int): ID of note
        :param TEXT (int): Text of note
        :param TAG (int): Tag of note
        :param DATE (time): Last date modified note
        """
        self.last_id = get_last_id()
        self.options = [("1", "Show all notes", self.display_note),
                        ("2", "Search notes", self.search_note),
                        ("3", "Add note", self.add_note),
                        ("4", "Modify note", self.modify_note),
                        ("5", "Quit", self.quit_notebook)]
        self.ID   = 0
        self.TEXT = 1
        self.TAG  = 2
        self.DATE = 3

    def add_note(self):
        """Name the text and tag for note.

        Input the text and tag for new note, then print out the time added note.
        :param: None.
        :return: None.
        """
        text = input("Enter a text: ")
        tag = input("Enter tag: ")

        self.update_notebook(text, tag)

        print("Your note has been added on", time.ctime())

    def update_notebook(self, text, tag=''):
        """Add a note to notebook.

        :param text (str): text for new note.
        :param tag (str): tag for new note (default is None).
        :return: None.
        """
        with open('notebook_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.last_id, text, tag, time.ctime()])

        self.last_id += 1

    def search_note(self):
        """Choose a note to search.

        Input the ID or text or tag of note you want to search,
        then call the function `search_in_notebook` to search for the selected note.
        :param: None.
        :return: None.
        """
        filt = input("Search for: ")
        temp_notebook = self.search_in_notebook(filt)
        self.display_note(temp_notebook)

    def search_in_notebook(self, filt):
        """Search for notes and return found notes.

        :param filt (str): The ID or the tag or the text has been selected for searching.
        :return: All the information of the note has been searched.
        """
        temp_notebook = []

        read_file = open("notebook_data.csv", "r")
        notebook = csv.reader(read_file)

        for note in notebook:
            if note[self.TEXT] == filt or note[self.TAG] == filt:
                temp_notebook.append(note)

        return temp_notebook

    def modify_note(self):
        """Choose a note to rename.

        Choose a new name to rename or not type anything to keep the old name.
        Input the note ID for modifying.
        Input new text for note.
        Input new tag for note.
        :param: None.
        :return: None.
        """
        temp_notebook = []

        read_file = open("notebook_data.csv", "r")
        notebook = csv.reader(read_file)

        for note in notebook:
            temp_notebook.append(note)

        while True:
            try:
                id = input("Enter a note id: ")
                if not id.isdigit() or int(id) >= self.last_id or int(id) < 1:
                    raise Exceptions.InvalidID
                break

            except Exceptions.InvalidID:
                print("Invalid ID, you've entered the ID bigger than the amount of notes or the ID doesn't exist.")

        for note in temp_notebook:
            if not note[self.ID] == id: continue
            old_text = note[self.TEXT]
            old_tag = note[self.TAG]

        while True:
            try:
                text = input("Enter a text: ")
                if text == old_text: raise Exceptions.InvalidText
                break

            except Exceptions.InvalidText:
                print("You entered an old text, please enter a new text.")

        while True:
            try:
                tag = input("Enter tag: ")
                if tag == old_tag: raise Exceptions.InvalidTag
                break

            except Exceptions.InvalidTag:
                print("You entered an old tag, please enter a new tag.")

        if text: self.modify_text(id, text)
        if tag: self.modify_tag(id, tag)


    def modify_text(self, id, text):
        """Rename text for note.

        :param note_id (int): The ID of the note need rename text.
        :param text (str): Name of the new text
        :return: None.
        """
        temp_notebook = []

        read_file = open("notebook_data.csv", "r")
        notebook = csv.reader(read_file)

        for row in notebook:
            if row[self.ID] == id:
                row[self.TEXT] = text
            temp_notebook.append(row)

        write_file = open("notebook_data.csv", "w", newline='')
        notebook = csv.writer(write_file)
        notebook.writerows(temp_notebook)

    def modify_tag(self, id, tag):
        """Rename text for note.

        :param note_id (int): The ID of the note need rename text.
        :param text (str): Name of the new text
        :return: None.
        """
        temp_notebook = []

        read_file = open("notebook_data.csv", "r")
        notebook = csv.reader(read_file)

        for row in notebook:
            if row[self.ID] == id:
                row[self.TAG] = tag
            temp_notebook.append(row)

        write_file = open("notebook_data.csv", "w", newline='')
        notebook = csv.writer(write_file)
        notebook.writerows(temp_notebook)

    def display_note(self, temp_notebook=None):
        """Display a single note or all the notes contained in the notebook.

        If no particular note is selected, show all notes.
        :param temp_notebook (list): Note want to show (default is None).
        :return: None.
        """

        if not temp_notebook:
            notebook_file = open("notebook_data.csv", "r")
            reader = csv.reader(notebook_file)
            for note in reader:
                print("Note ID:", note[self.ID], "\n"
                      "Note tag:", note[self.TEXT], "\n"
                      "Note text:", note[self.TAG], "\n"
                      "Last modified on:", note[self.DATE], "\n")

        else:
            for note in temp_notebook:
                print("Note ID:", note[self.ID], "\n"
                      "Note tag:", note[self.TEXT], "\n"
                      "Note text:", note[self.TAG], "\n"
                      "Last modified on:", note[self.DATE], "\n")

    def display_menu(self):
        """Display notebook menu options.

        :param: None
        :return: None
        """
        print(ENDLINE)
        print("Notes menu:")

        for option in self.options:
            print(option[0] + ". " + option[1])

    def quit_notebook(self):
        """Quit the program.

        :param: None
        :return: None
        """
        print("Thank you for using your Notebook today.")
        sys.exit(0)

if __name__ == "__main__":

    Notebook_1 = Notebook()

    while True:
        Notebook_1.display_menu()
        option = input("Enter an option: ")
        action = None

        for choice in Notebook_1.options:
            if option == choice[0]: action = choice[2]

        try:
            if action:
                print(ENDLINE)
                action()
            else:
                raise Exceptions.InvalidChoice

        except Exceptions.InvalidChoice:
            print(f"'{option}' is not a valid choice")
