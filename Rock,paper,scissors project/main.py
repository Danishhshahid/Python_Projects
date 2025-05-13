import random
emojis = {
    "r" : "🪨",
    "s" : "✂️",
    "p": "📄"
}
choices = ('r','p','s')

while True:
    user_choice = input("rock, paper,scissors (r/p/s): ").lower()
    if user_choice not in choices:
        print("Invalid Choice!")
        continue

    computer_choice =  random.choice(choices)

    print(f"you chose {emojis[user_choice]}")
    print(f"Computer chose: {emojis[computer_choice]}")

    if user_choice == computer_choice:
        print("tie")
    elif (user_choice == "r" and computer_choice == "s") or (user_choice == "s" and computer_choice == "p" or (user_choice == "p" and computer_choice == "r")):
        print("you win")
    else:
        print("you loose")


    should_continue = input("Continue (y/n): ").lower()
    if should_continue == "n":
        break


