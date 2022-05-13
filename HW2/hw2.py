import sys
import datetime
import time
from Exceptions_hw2 import CustomException
endline = "_"*80

class Note():
    def __init__(self, text, tag, day, id):
        self.text = text
        self.tag = tag
        self.day = day
        self.id = id

class Notebook():
    def __init__(self):
        self.last_id = 1
        self.list_notes = []
        self.options = [("1", "Show all notes", self.Note_Display),
                        ("2", "Search notes", self.Note_Searching),
                        ("3", "Add note", self.Note_Addition),
                        ("4", "Modify note", self.Modification),
                        ("5", "Quit", self.quit)]
        self.all_note = self.list_notes

    def Addition(self, text, tags=''):
        self.list_notes.append(Note(text,
                                    tags,
                                    datetime.datetime.now(),
                                    self.last_id))
        self.last_id += 1

    def Note_Addition(self):
        text = input("Enter a text: ")
        tags = input("Enter tag: ")
        self.Addition(text, tags)
        print("Your note has been added on", time.ctime())

    def Note_Searching(self):
        filter = input("Search for: ")
        list_notes = self.Searching(filter)
        self.Note_Display(list_notes)

    def Searching(self, filter):
        return [note for note in self.list_notes
                if filter in note.text
                or filter in note.tag]

    def Modification(self):
        id = input("Enter a note id: ")
        if not id.isdigit() or int(id) >= self.last_id:
            raise CustomException.InvalidID()

        for note in self.list_notes:
            if not note.id == int(id): continue
            old_text = note.text
            old_tag = note.tag

        text = input("Enter a text: ")
        if text == old_text: raise CustomException.InvalidText()
        tag = input("Enter tags: ")
        if tag == old_tag: raise CustomException.InvalidTag()

        if text: self.Text_Modification(id, text)
        if tag: self.Tag_Modification(id, tag)

    def Tag_Modification(self, note_id, tag):
        for note in self.list_notes:
            if not note.id == int(note_id): continue

            note.tag = tag
            note.day = datetime.datetime.now()
            break

    def Text_Modification(self, note_id, text):
        for note in self.list_notes:
            if not note.id == int(note_id): continue

            note.text = text
            note.day = datetime.datetime.now()
            break

    def Note_Display(self, note_searched=None):
        if not note_searched: note_searched = self.all_note
        note_searched = sorted(note_searched, key=lambda note: note.day)
        for note in note_searched:
            print(
f"""Note id: {note.id}
Note tags: {note.tag}
Note text: {note.text}
Last modified on: {note.day.strftime('%X, %A, %x')}
""")

    def Menu_Display(self):
        print(endline)
        print("Notes menu:")
        for option in self.options:
            print(option[0] + ". " + option[1])

    def quit(self):
        print("Thank you for using your Notebook today.")
        sys.exit(0)

if __name__ == "__main__":
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

