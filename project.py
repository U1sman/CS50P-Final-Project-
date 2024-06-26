import roles
import passwords
import questionary
import random
import pyfiglet
import csv
import sys
from colorama import init, Fore, Style
from termcolor import colored
# make bold/colour styles work on cmd
init()

def main():
    ascii_art = pyfiglet.figlet_format("PYTHON GROCERY STORE", font="small")
    colored_ascii_art = colored(ascii_art, color="magenta")
    print(colored_ascii_art)
    role_option = questionary.select(
    "Choose a Role:",
    choices=[
        "Owner",
        "Customer"
    ]).ask()
    if role_option == "Owner":
        owner()
    else: customer()


def owner():
    storename = passwords.password()
    while True:
        try:
            action = str(input("Action: ").lower().strip())
            owner_class = roles.Owner(action, storename)
            owner_action(action, owner_class)
        except (ValueError, EOFError):
            print(roles.bold("Please enter a valid action"))


def customer():
    storename = random_store()
    while True:
        try:
            action = str(input("Action: ").lower().strip())
            customer_class = roles.Customer(action, storename)
            customer_action(action, customer_class)
        except (ValueError, EOFError):
            print(roles.bold("Please enter a valid action"))


def owner_action(action, owner_class):
    match action:
        case "add"|"a":
            owner_class.add_item()
        case "delete"|"d":
            owner_class.delete_item()
        case "change-price"|"c":
            owner_class.change_price()
        case "restock"|"r":
            owner_class.restock()
        case "help"|"h":
            owner_class.help()
        case "exit"|"e":
            owner_class.exit()
        case r"\\d\\":
            owner_class.delete_store()
        case "profit"|"p":
            owner_class.view_profit()
        case "budget"|"b":
            owner_class.view_budget()
        case "view"|"v":
            owner_class.view_items()
        case "leaderboard"|"l":
            owner_class.view_leaderboard()
        case _:
            print(roles.bold("Please enter a valid action"))


def customer_action(action, customer_class):
    match action:
        case "help"|"h":
            customer_class.customer_help()
        case "exit"|"e":
            customer_class.exit()
        case "view"|"v":
            customer_class.view_items()
        case "buy"|"b":
            customer_class.buy_items()
        case "review"|"r":
            customer_class.review()
        case _:
            print(roles.bold("Please enter a valid action"))


def random_store() -> str:
    storenames = []
    with open(f"csvs\\passwords.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            storenames.append(row["storename"])
    if not storenames:
        sys.exit("-------------------\n\033[91m\033[1mNo Stores available\033[0m\n-------------------")
    storename = random.choice(storenames) 
    print(roles.bold(f"                                      You are at '{storename}' store"))
    return storename   


if __name__ == "__main__":
    main()