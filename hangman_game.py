import random

print("Welcome to Hangman")
print("------------------")
print("    --       -- ")
print(" --     --     -- ")
print("   --        --    ")
print("      --  --     ")
print("        -- ")

# Dictionary containing word categories and their associated words
word_categories = {
    1: ["ferrari", "mercedes", "bmw", "audi", "bugatti", "hyundai", "honda"],
    2: ["rose", "daisy", "sunflower", "tulip", "lily"],
    3: ["india", "usa", "canada", "australia", "japan"],
    4: ["apple", "banana", "orange", "grape", "strawberry"],
    5: ["dog", "cat", "bird", "fish", "rabbit"],
    6: ["football", "basketball", "tennis", "soccer", "volleyball"],
    7: ["mountain", "ocean", "desert", "forest", "river"]
}

# Function to choose a word category
def choose_category():
    print("Choose a category:")
    print("1. Cars")
    print("2. Flowers")
    print("3. Countries")
    print("4. Fruits")
    print("5. Animals")
    print("6. Sports")
    print("7. Natural Landscapes")
    choice = int(input("Enter your choice: "))
    return choice

# Function to choose a random word from the selected category
def choose_word(category):
    if category in word_categories:
        return random.choice(word_categories[category])
    else:
        print("Invalid category")
        return None

# Function to print the hangman figure based on the number of wrong guesses
def print_hangman(wrong):
    if wrong == 0:
        print("\n+---+")
        print("    |")
        print("    |")
        print("    |")
        print("   ===")
    elif wrong == 1:
        print("\n+---+")
        print("O   |")
        print("    |")
        print("    |")
        print("   ===")
    elif wrong == 2:
        print("\n+---+")
        print("O   |")
        print("|   |")
        print("    |")
        print("   ===")
    elif wrong == 3:
        print("\n+---+")
        print(" O  |")
        print("/|  |")
        print("    |")
        print("   ===")
    elif wrong == 4:
        print("\n+---+")
        print(" O  |")
        print("/|\ |")
        print("    |")
        print("   ===")
    elif wrong == 5:
        print("\n+---+")
        print(" O  |")
        print("/|\ |")
        print("/   |")
        print("   ===")
    elif wrong == 6:
        print("\n+---+")
        print(" O   |")
        print("/|\  |")
        print("/ \  |")
        print("    ===")

# Function to print the word with correctly guessed letters
def print_word(word, guessed_letters):
    for char in word:
        if char in guessed_letters:
            print(char, end=" ")
        else:
            print("_", end=" ")

# Function to play the hangman game
def play_hangman():
    while True:
        category = choose_category()
        selected_word = choose_word(category)
        if selected_word is None:
            return

        guessed_letters = []
        wrong_guesses = 0

        while wrong_guesses < 6:
            print("\nWord to guess: ", end="")
            print_word(selected_word, guessed_letters)

            if all(letter in guessed_letters for letter in selected_word):
                print("\nCongratulations! You've guessed the word:", selected_word)
                break

            print_hangman(wrong_guesses)
            guess = input("\nGuess a letter: ").lower()

            if guess in guessed_letters:
                print("You've already guessed that letter!")
            elif guess in selected_word:
                print("Good guess!")
                guessed_letters.append(guess)
            else:
                print("Incorrect guess!")
                wrong_guesses += 1

        if wrong_guesses == 6:
            print("Sorry, you've run out of tries. The word was:", selected_word)

        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != 'yes':
            break

# Main function
def main():
    play_hangman()

if __name__ == "__main__":
    main()
