import sys
import datetime
import time
import sqlite3
from Exceptions import CustomException
endline = "_"*80

def DBCreate():
    """Create a database connection to the SQLite database.

    :param: None
    :return: None
    """
    global connection, cursor
    connection = sqlite3.connect("NotebookData.db")
    cursor = connection.cursor()
    cursor.execute("create table if not exists Notebook (ID integer, TEXT text, TAG text, DAY_CREATED)")

def get_last_id():
    """Get the ID of the last note added to the table Notebook.

    :param: None
    ":return" None
    """
    record = cursor.execute("SELECT ID FROM Notebook ORDER BY ID DESC LIMIT 1").fetchone()
    return 1 if record == None else record[0]+1

def update_text(conn, text):
    """Update the text at a specified position in the table Notebook.

    :param conn (sqlite3.Connection):
    :param text (str):
    :return: None
    """
    sql = ''' UPDATE Notebook SET TEXT = ?, DAY_CREATED = ?  WHERE ID = ?'''
    cur = conn.cursor()
    cur.execute(sql, text)
    conn.commit()

def update_tag(conn, tag):
    """Update the tag at a specified position in the table Notebook.

    :param conn (sqlite3.Connection):
    :param tag (str):
    :return: None
    """
    sql = ''' UPDATE Notebook SET TAG = ?, DAY_CREATED = ?  WHERE ID = ?'''
    cur = conn.cursor()
    cur.execute(sql, tag)
    conn.commit()

class Note():
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

class Notebook():
    """Class contains all the notes.

        Create a menu of options for queries with notebook.

        Methods:

            Addition(text, tags=''):
                Add a note to notebook.

            Note_Addition():
                Name the text and tag for note.

            Searching(filter):
                Choose a note to search.

            Note_Searching():
                Search for notes and return found notes.

            Modification():
                Choose a note to rename and type new text, new tag.

            Tag_Modification(note_id, tag):
                Rename tag for note.

            Text_Modification(note_id, text):
                Rename text for note.

            Note_Display(note_searched=None):
                Display a single note or all the notes contained in the notebook.

            Menu_Display():
                Display notebook menu options.

            quit():
                Exit the program.
        """
    def __init__(self):
        """Inits notebook.

        :param last_id (int): the ID for the newly added note.
        :param list_notes (str): the List contains all the note added.
        :param options (list): the menu of the notebook.
        :param all_note (list): all notes have been added before.
        """
        self.last_id = get_last_id()
        self.list_notes = []
        self.options = [("1", "Show all notes", self.Note_Display),
                        ("2", "Search notes", self.Note_Searching),
                        ("3", "Add note", self.Note_Addition),
                        ("4", "Modify note", self.Modification),
                        ("5", "Quit", self.Quit)
                        ]
        self.all_note = self.list_notes

    def Addition(self, text, tags=''):
        """Add a note to notebook.

        :param text (str): text for new note.
        :param tags (str): tag for new note (default is None).
        :return: None.
        """
        self.list_notes.append(Note(text,
                                    tags,
                                    datetime.datetime.now(),
                                    self.last_id
                                    ))
        cursor.executemany("INSERT INTO Notebook VALUES (?,?,?,?)", [(self.last_id,
                                                                  text,
                                                                  tags,
                                                                  time.ctime()
                                                                  )])
        connection.commit()
        self.last_id += 1

    def Note_Addition(self):
        """Name the text and tag for note.

        Input the text and tag for new note, then print out the time added note.
        :param: None.
        :return: None.
        """
        text = input("Enter a text: ")
        tags = input("Enter tag: ")
        self.Addition(text, tags)
        print("Your note has been added on", time.ctime())

    def Note_Searching(self):
        """Choose a note to search.

        Input the ID or text or tag of note you want to search,
        then call the function `seaching` to search for the selected note.
        :param: None.
        :return: None.
        """
        filter = input("Search for: ")
        list_notes = self.Searching(filter)
        self.Note_Display(list_notes)

    def Searching(self, filt):
        """Search for notes and return found notes.

        :param filter (str): The ID or the tag or the text has been selected for searching.
        :return: All the information of the note has been searched.
        """
        note_searched = cursor.execute("select * from Notebook where TEXT=? or TAG=?", (filt, filt,)).fetchall()
        return note_searched

    def Modification(self):
        """Choose a note to rename.

        Choose a new name to rename or not type anything to keep the old name.
        Input the note ID for modify.
        Input new text for note.
        Input new tag for note.
        :param: None.
        :return: None.
        """
        id = input("Enter a note id: ")
        if not id.isdigit() or int(id) >= self.last_id:
            raise CustomException.InvalidID()

        old_text = cursor.execute("SELECT TEXT from Notebook WHERE ID = ?", id).fetchone()
        old_text = old_text[0]

        old_tag = cursor.execute("SELECT TAG from Notebook WHERE ID = ?", id).fetchone()
        old_tag = old_tag[0]

        text = input("Enter a text: ")
        if text == old_text: raise CustomException.InvalidText()
        tag = input("Enter tags: ")
        if tag == old_tag: raise CustomException.InvalidTag()

        if text: self.Text_Modification(int(id), text)
        if tag: self.Tag_Modification(int(id), tag)

    def Tag_Modification(self, note_id, tag):
        """Rename tag for note.

        :param note_id (int): The ID of the note need rename tag.
        :param tags (str): Name of the new tag.
        :return: None.
        """
        update_tag(connection, (tag, datetime.datetime.now(), note_id))

    def Text_Modification(self, note_id, text):
        """Rename text for note.

        :param note_id (int): The ID of the note need rename text.
        :param text (str): Name of the new text
        :return: None.
        """
        update_text(connection, (text, datetime.datetime.now(), note_id))

    def Note_Display(self, note_searched=None):
        """Display a single note or all the notes contained in the notebook.

        If no particular note is selected, show all notes.
        :param note_searched (list): Note want to show (default is None).
        :return: None.
        """
        if not note_searched:
            for note in cursor.execute("SELECT * FROM Notebook"):
                print(
f"""Note ID: {note[0]}
Note tags: {note[1]}
Note text: {note[2]}
Last modified on: {note[3]}
""")

        else:
            for note in note_searched:
                print(
f"""Note ID: {note[0]}
Note tags: {note[1]}
Note text: {note[2]}
Last modified on: {note[3]}
""")

    def Menu_Display(self):
        """Display notebook menu options.

        :param: None
        :return: None
        """
        print(endline)
        print("Notes menu:")
        for option in self.options:
            print(option[0] + ". " + option[1])

    def Quit(self):
        """Quit the program.

        :param: None
        :return: None
        """
        print("Thank you for using your Notebook today.")
        sys.exit(0)
        connection.close()

if __name__ == "__main__":
    DBCreate()
    Notebook_1 = Notebook()

    while True:
        Notebook_1.Menu_Display()
        option = input("Enter an option: ")
        action = None
        for choice in Notebook_1.options:
            if option == choice[0]: action = choice[2]

        if action:
            print(endline)
            action()
        else:
            raise CustomException.InvalidChoice(option)

