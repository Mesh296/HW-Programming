import sys
import datetime
import time
import MyExceptions
ENDLINE = "_" * 80

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
        self.options = [("1", "Show all notes", self.display_note),
                        ("2", "Search notes", self.search_note),
                        ("3", "Add note", self.add_note),
                        ("4", "Modify note", self.modifiy_note),
                        ("5", "Quit", self.quit_notebook)]
        self.all_note = self.list_notes

    def adding(self, text, tags=''):
        self.list_notes.append(Note(text,
                                    tags,
                                    datetime.datetime.now(),
                                    self.last_id))
        self.last_id += 1

    def add_note(self):
        text = input("Enter a text: ")
        tags = input("Enter tag: ")
        self.adding(text, tags)
        print("Your note has been added on", time.ctime())

    def search_note(self):
        filter = input("Search for: ")
        list_notes = self.searching(filter)
        self.display_note(list_notes)

    def searching(self, filter):
        return [note for note in self.list_notes
                if filter in note.text
                or filter in note.tag]

    def modifiy_note(self):
        while True:
            try:
                id = input("Enter a note id: ")
                if not id.isdigit() or int(id) >= self.last_id or int(id) < 1:
                    raise MyExceptions.InvalidID
                break
            except MyExceptions.InvalidID:
                print("Invalid ID, you've entered the ID bigger than the amount of notes or the ID doesn't exist.")

        for note in self.list_notes:
            if not note.id == int(id): continue
            old_text = note.text
            old_tag = note.tag

        while True:
            try:
                text = input("Enter a text: ")
                if text == old_text: raise MyExceptions.InvalidText
                break
            except MyExceptions.InvalidText:
                print("You entered an old text, please enter a new text.")

        while True:
            try:
                tag = input("Enter tag: ")
                if tag == old_tag: raise MyExceptions.InvalidTag
                break
            except MyExceptions.InvalidTag:
                print("You entered an old tag, please enter a new tag.")

        if text: self.modify_text(id, text)
        if tag: self.modify_tag(id, tag)

    def modify_tag(self, note_id, tag):
        for note in self.list_notes:
            if not note.id == int(note_id): continue

            note.tag = tag
            note.day = datetime.datetime.now()
            break

    def modify_text(self, note_id, text):
        for note in self.list_notes:
            if not note.id == int(note_id): continue

            note.text = text
            note.day = datetime.datetime.now()
            break

    def display_note(self, note_searched=None):
        if not note_searched: note_searched = self.all_note
        note_searched = sorted(note_searched, key=lambda note: note.day)
        for note in note_searched:
            print(
f"""Note id: {note.id}
Note tag: {note.tag}
Note text: {note.text}
Last modified on: {note.day.strftime('%X, %A, %x')}
""")

    def display_menu(self):
        print(ENDLINE)
        print("Notes menu:")
        for option in self.options:
            print(option[0] + ". " + option[1])

    def quit_notebook(self):
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
                raise MyExceptions.InvalidChoice
        except MyExceptions.InvalidChoice:
            print(f"'{option}' is not a valid choice")


