class CustomException():

    class InvalidChoice(Exception):
        def __init__(self, choice):
            self.choice = choice

        def __str__(self):
            return f"{self.choice} is not a valid choice"

    class InvalidID(Exception):
        def __str__(self):
            return f"Invalid ID, you've entered the ID bigger than the amount of notes."

    class InvalidTag(Exception):
        def __str__(self):
            return f"You entered an old tag, please enter a new tag."

    class InvalidText(Exception):
        def __str__(self):
            return f"You entered an old text, please enter a new text."
