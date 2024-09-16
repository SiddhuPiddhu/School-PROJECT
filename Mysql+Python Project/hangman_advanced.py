import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import random

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'hangman_game'
}

class HangmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")

        self.username_label = tk.Label(root, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        self.password_label = tk.Label(root, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, show='*')
        self.password_entry.pack()

        self.register_button = tk.Button(root, text="Register", command=self.register)
        self.register_button.pack()

        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.pack()

        self.exit_button = tk.Button(root, text="Exit", command=root.quit)
        self.exit_button.pack()

    def create_connection(self):
        """Create a database connection."""
        try:
            connection = mysql.connector.connect(**db_config)
            if connection.is_connected():
                return connection
        except Error as e:
            messagebox.showerror("Error", f"Database connection error: {e}")
        return None

    def close_connection(self, connection):
        """Close the database connection."""
        if connection.is_connected():
            connection.close()

    def register(self):
        """Register a new player."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        connection = self.create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("INSERT INTO players (username, password) VALUES (%s, %s)", (username, password))
                connection.commit()
                messagebox.showinfo("Registration", "Registration successful.")
            except Error as e:
                messagebox.showerror("Error", f"Registration error: {e}")
            finally:
                self.close_connection(connection)

    def login(self):
        """Login an existing player."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        connection = self.create_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id, high_score FROM players WHERE username = %s AND password = %s", (username, password))
            result = cursor.fetchone()
            self.close_connection(connection)
            if result:
                player_id, high_score = result
                messagebox.showinfo("Login", f"Login successful. Your high score is {high_score}.")
                self.play_game(player_id, high_score)
            else:
                messagebox.showerror("Error", "Invalid username or password.")

    def play_game(self, player_id, high_score):
        """Play the hangman game."""
        words = ['python', 'mysql', 'database', 'programming', 'hangman']
        word = random.choice(words)
        guessed_word = ['_'] * len(word)
        guessed_letters = set()
        attempts = 7

        hangman_frame = tk.Frame(self.root)
        hangman_frame.pack()

        hangman_label = tk.Label(hangman_frame, text=" ".join(guessed_word))
        hangman_label.pack()

        guessed_word_label = tk.Label(self.root, text="")
        guessed_word_label.pack()

        attempts_label = tk.Label(self.root, text=f"Remaining attempts: {attempts}")
        attempts_label.pack()

        hangman_ascii_label = tk.Label(self.root, text="")
        hangman_ascii_label.pack()

        def print_hangman(attempts):
            """Print ASCII art of hangman."""
            if attempts == 7:
                hangman_ascii_label.config(text=
                    "+---+\n"
                    "    |\n"
                    "    |\n"
                    "    |\n"
                    "   ==="
                )
            elif attempts == 6:
                hangman_ascii_label.config(text=
                    "+---+\n"
                    "O   |\n"
                    "    |\n"
                    "    |\n"
                    "   ==="
                )
            elif attempts == 5:
                hangman_ascii_label.config(text=
                    "+---+\n"
                    "O   |\n"
                    "|   |\n"
                    "    |\n"
                    "   ==="
                )
            elif attempts == 4:
                hangman_ascii_label.config(text=
                    "+---+\n"
                    " O  |\n"
                    "/|  |\n"
                    "    |\n"
                    "   ==="
                )
            elif attempts == 3:
                hangman_ascii_label.config(text=
                    "+---+\n"
                    " O  |\n"
                    "/|\ |\n"
                    "    |\n"
                    "   ==="
                )
            elif attempts == 2:
                hangman_ascii_label.config(text=
                    "+---+\n"
                    " O  |\n"
                    "/|\ |\n"
                    "/   |\n"
                    "   ==="
                )
            elif attempts == 1:
                hangman_ascii_label.config(text=
                    "+---+\n"
                    " O   |\n"
                    "/|\  |\n"
                    "/ \  |\n"
                    "    ==="
                )

        def make_guess():
            guess = guess_entry.get().lower()
            if guess in guessed_letters:
                messagebox.showinfo("Duplicate Guess", "You already guessed that letter. Try again.")
            elif guess in word:
                messagebox.showinfo("Good Guess", "Good guess!")
                for i, letter in enumerate(word):
                    if letter == guess:
                        guessed_word[i] = guess
                hangman_label.config(text=" ".join(guessed_word))
            else:
                nonlocal attempts
                attempts -= 1
                attempts_label.config(text=f"Remaining attempts: {attempts}")
                print_hangman(attempts)
                if attempts == 0:
                    messagebox.showinfo("Game Over", f"Game over. The word was: {word}")
                    hangman_frame.destroy()
                else:
                    messagebox.showinfo("Wrong Guess", "Incorrect guess. Try again.")

            guessed_letters.add(guess)
            guess_entry.delete(0, tk.END)

            if '_' not in guessed_word:
                messagebox.showinfo("Congratulations", "Congratulations! You guessed the word.")
                score = attempts
                if score > high_score:
                    messagebox.showinfo("New High Score", "New high score!")
                    self.update_high_score(player_id, score)

        guess_label = tk.Label(self.root, text="Guess a letter:")
        guess_label.pack()

        guess_entry = tk.Entry(self.root)
        guess_entry.pack()

        guess_button = tk.Button(self.root, text="Guess", command=make_guess)
        guess_button.pack()

    def update_high_score(self, player_id, score):
        """Update the high score of a player."""
        connection = self.create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("UPDATE players SET high_score = %s WHERE id = %s", (score, player_id))
                connection.commit()
            except Error as e:
                messagebox.showerror("Error", f"Update high score error: {e}")
            finally:
                self.close_connection(connection)

def main():
    root = tk.Tk()
    app = HangmanGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
