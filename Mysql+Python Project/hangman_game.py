import mysql.connector
from mysql.connector import Error
import random
import getpass

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'hangman_game'
}

def create_connection():
    """Create a database connection."""
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
    return None

def close_connection(connection):
    """Close the database connection."""
    if connection.is_connected():
        connection.close()

def register(username, password):
    """Register a new player."""
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO players (username, password) VALUES (%s, %s)", (username, password))
            connection.commit()
            print("Registration successful.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            close_connection(connection)

def login(username, password):
    """Login an existing player."""
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id, high_score FROM players WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        close_connection(connection)
        if result:
            return result[0], result[1]
    return None, None

def update_high_score(player_id, score):
    """Update the high score of a player."""
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("UPDATE players SET high_score = %s WHERE id = %s", (score, player_id))
        connection.commit()
        close_connection(connection)

        
def print_hangman(attempts): 
    if attempts == 7: 
        print("\n+---+") 
        print("    |") 
        print("    |") 
        print("    |") 
        print("   ===") 
    elif attempts == 6: 
        print("\n+---+") 
        print("O   |") 
        print("    |") 
        print("    |") 
        print("   ===") 
    elif attempts == 5: 
        print("\n+---+") 
        print("O   |") 
        print("|   |") 
        print("    |") 
        print("   ===") 
    elif attempts == 4: 
        print("\n+---+") 
        print(" O  |") 
        print("/|  |") 
        print("    |") 
        print("   ===") 
    elif attempts == 3: 
        print("\n+---+") 
        print(" O  |") 
        print("/|\ |") 
        print("    |") 
        print("   ===") 
    elif attempts == 2: 
        print("\n+---+") 
        print(" O  |") 
        print("/|\ |") 
        print("/   |") 
        print("   ===") 
    elif attempts == 1: 
        print("\n+---+") 
        print(" O   |") 
        print("/|\  |") 
        print("/ \  |") 
        print("    ===")
        
def play_game(player_id, high_score):
    """Play the hangman game."""
    words = ['python', 'mysql', 'database', 'programming', 'hangman']
    word = random.choice(words)
    guessed_word = ['_'] * len(word)
    guessed_letters = set()
    attempts = 7

    print("\nWelcome to Hangman!")
    print(" ".join(guessed_word))

    while attempts > 0 and '_' in guessed_word:
        guess = input("Guess a letter: ").lower()
        if guess in guessed_letters:
            print("You already guessed that letter. Try again.")
        elif guess in word:
            print("Good guess!")
            for i, letter in enumerate(word):
                if letter == guess:
                    guessed_word[i] = guess
        else:
            print_hangman(attempts)
            attempts -= 1
        guessed_letters.add(guess)
        print(f"Guessed word: {' '.join(guessed_word)}")
        print(f"Remaining attempts: {attempts}")

    if '_' not in guessed_word:
        print("Congratulations! You guessed the word.")
        score = attempts
        if score > high_score:
            print("New high score!")
            update_high_score(player_id, score)
    else:
        print(f"Game over. The word was: {word}")

def main():
    while True:
        print("\nNumber Guessing Game")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter a username: ")
            password = input("Enter a password: ")  # Temporary workaround
            register(username, password)
        elif choice == '2':
            username = input("Enter your username: ")
            password = input("Enter your password: ")  # Temporary workaround
            player_id, high_score = login(username, password)
            if player_id:
                print(f"Login successful. Your high score is {high_score}.")
                play_game(player_id, high_score)
            else:
                print("Invalid username or password.")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
