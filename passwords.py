import questionary
import csv
import sys
from roles import bold
from colorama import init, Fore, Style
# make bold/colour styles work on cmd
init()
password_path = 'csvs\\passwords.csv'

def password() -> list:
    log = "Log Into Existing Store"
    sign = "Create New Store"

    ls = questionary.select(
    "LOGIN/SIGNUP",
    choices=[
        log,
        sign,
        "Exit",
    ]).ask()
    if ls == log: return login()
    elif ls == sign: return signup()
    elif ls == "Exit": sys.exit(bold("Goodbye!"))
    

def login() -> list:
        while True:
            try:
                stornm_input = input("Storename(/e for exit): ").strip()
                if stornm_input == "/e":
                    sys.exit(bold("Goodbye!"))
                pswrd_input = input("Password(/e for exit): ").strip()
                if pswrd_input == "/e":
                    sys.exit(bold("Goodbye!"))

                if login_authenticator(stornm_input, pswrd_input):
                    print(f"                                      \033[1mLogged in as '{stornm_input}'\033[0m")
                    return stornm_input
                else: print("-----------------------------------\n\033[91m\033[1mStore Name or Password Is Incorrect\033[0m\033[0m\n-----------------------------------")
            except (EOFError,ValueError):
                pass


def signup() -> list:
    while True:
            try:
                stornm_input = input("Storename(/e for exit): ").strip()
                if stornm_input == "/e":
                    sys.exit(bold("Goodbye!"))
                pswrd_input = input("Password(/e for exit): ").strip()
                if pswrd_input == "/e":
                    sys.exit(bold("Goodbye!"))

                if signup_authenticator(stornm_input, pswrd_input) == "created":
                    print(f"                                      \033[1mCreated '{stornm_input}'\033[0m")
                    create_item_file(stornm_input)
                    create_leaderboard(stornm_input)
                    return stornm_input
                elif signup_authenticator(stornm_input, pswrd_input) == "no":
                    print("---------------------------\n\033[91m\033[1mEnter a valid Name/Password\033[0m\033[0m\n---------------------------")
                elif not signup_authenticator(stornm_input, pswrd_input) == "exists": 
                    print("--------------------\n\033[91m\033[1mStore Already Exists\033[0m\033[0m\n--------------------")
            except (EOFError,ValueError):
                pass
         

def login_authenticator(stornm, pswrd) -> bool:
    with open(password_path) as passwords_file:
        passwords = csv.DictReader(passwords_file)
        for row in passwords:
            if row["storename"] == stornm and row["password"] == pswrd:
                return True
    return False


def signup_authenticator(stornm, pswrd)-> bool:
    if stornm == "" or pswrd == "":
        return "no"
    with open(password_path) as passwords_file:
        passwords = csv.DictReader(passwords_file)
        store_exists = False
        for row in passwords:
            if stornm == row["storename"]:
                store_exists = True
                break 
        if not store_exists:
            with open(password_path, "a", newline="") as file:
                passwords_writer = csv.DictWriter(file, fieldnames=["storename", "password"]) 
                passwords_writer.writerow({"storename": stornm, "password": pswrd})
            return "created"
        else:
            return "exists"
                 

def create_item_file(store) -> str:
    item_path = f"csvs\\{store}_data.csv"
    fieldnames = ['item_name', 'quantity', 'price', 'profit', 'budget']
    default_values = {'item_name': None, 'quantity': None, 'price': None, 'profit': 0.00, 'budget': 1000.00}
    with open(item_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(default_values)


def create_leaderboard(store):
    fieldnames = ['storename', 'budget']
    # Read store data CSV and extract relevant rows
    store_data = []
    with open(f"csvs\\{store}_data.csv", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            store_data.append({'storename': store, 'budget': row["budget"]})

    # Write or append to leaderboard CSV
    with open("csvs\\leaderboard.csv", "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write header only if the file is empty
        if file.tell() == 0:
            writer.writeheader()

        # Write all rows from store data
        writer.writerows(store_data)
    