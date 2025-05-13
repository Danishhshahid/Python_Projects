import random
import string
from words import words



def get_valid_word(words):
    word = random.choice(words)

    while '-' in word or ' ' in word:
        word = random.choice(words)
    return word



def hangman():
    word = get_valid_word(words).upper()
    word_letters = set(word)
    alphabet = set(string.ascii_uppercase)
    used_letters = set()

    lives = 6

    while len(word_letters) > 0 and lives > 0 :

        print("you have",lives," lives left and you have used these letter",' '.join(used_letters))
        word_list = [letter if letter in used_letters else '-' for letter in word]
        print("Current word : "," ".join(word_list))



        user_letter = input("Guess a letter: ").upper()
        if user_letter in alphabet - used_letters:
            used_letters.add(user_letter)
            if user_letter in word_letters:
                word_letters.remove(user_letter)
            else:
                lives = lives - 1
                print("letter is not in words")



        elif user_letter in used_letters:
            print("You have already that character , please try again")
        else:
            print("Invalid Character, please try again")


    if lives == 0:
        print("you died")
    else:
        print(f"\n🎉 You guessed the word correctly: {word} 🎉")

hangman()