import sys
import csv
import tabulate
import questionary
import os
import numpy as np
from colorama import init, Fore, Style
# make bold/colour styles work on cmd

init()

def bold(text):
    return f"\033[1m{text}\033[0m"

def set_price(itemname):
    while True:
        try:
            price = np.float64(input(f"Set Price(per unit cost: {items_addable_prices[itemname]/100}): "))
            print(f"{bold("Set price to")} '{Fore.BLUE}{bold(price)}{Style.RESET_ALL}'")
            return price
        except (EOFError, ValueError):
            continue

items_addable_table = {
    #Items should not be below 20 in price
    #Make sure to add roll number, item_name, quantity to 100(not more or less)
    #Make sure to change items_addable_prices aswell 
    "": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21","22"],
    "Item": ["Apples","Bananas","Bread","Milk","Eggs","Chicken breasts","Ground beef","Butter","Cheese","Yogurt","Carrots","Tomatoes","Lettuce","Potatoes","Rice","Pasta","Canned beans","Cereal","Orange juice","Coffee","Sugar","Salt"],
    "Quantity": ["100", "100", "100", "100", "100", "100", "100", "100", "100", "100", "100", "100", "100", "100", "100", "100", "100", "100", "100", "100","100","100"],
    "Price": ["50", "40", "100", "120", "80", "250", "300", "150", "200", "130", "30", "45", "25", "60", "70", "90", "55", "110", "180", "220","120","120"],
    }

commands_owner = [bold("'add'/'a'"), bold("'delete'/'d'"), bold("'change-price'/'c'"), bold("'restock'/'r'"), bold("'profit'/'p'"), bold("'budget'/'b'"), bold("'view'/'v'"), bold("'leaderboard'/'l'"), bold("'help'/'h'"), bold("'exit'/'e'"), bold(r"'\\d\\'")]
commands_customer = [bold("'help'/'h'"), bold("'view'/'v'"), bold("'buy'/'b'"), bold("'review'/'r'"), bold("'exit'/'e'")]
help_table = {
    "Commands": commands_owner, 
    "Info": [
        "Add Item to store",
        "Delete Item from store",
        "Change Price of an item",
        "Restock existing items",
        "View Current Profit",
        "View Current Budget",
        "View items in store",
        "View Leaderboard",
        "View commands",
        "Exit the program",
        "Delete store"
    ]
}

help_table_customer = {
    "Commands": commands_customer,
    "Info": [
        "View commands",
        "View items in store",
        "Buy items from store",
        "Leave positive/negative feedback",
        "Exit the program"
    ]
}

items_addable_prices = {
    #Items should not be below 20 in price
    "Apples":50,
    "Bananas":40,
    "Bread":100,
    "Milk":120,
    "Eggs":80,
    "Chicken breasts":250,
    "Ground beef":300,
    "Butter":150,
    "Cheese":200,
    "Yogurt":130,
    "Carrots":30,
    "Tomatoes":45,
    "Lettuce":25,
    "Potatoes":60,
    "Rice":70,
    "Pasta":90,
    "Canned beans":55,
    "Cereal":110,
    "Orange juice":180,
    "Coffee":220,
    "Sugar":120,
    "Salt":120
}


class Owner:
    def __init__(self, action:str=None, storename=None) -> None:
        self.action = action
        self.storename = storename
        if self.check_bankrupt():
            self.delete_store()
        self.update_leaderboard_budget()

    @property
    def action(self):
        return self._action
    
    @action.setter
    def action(self, action):
        self._action = action

    @property
    def storename(self):
        return self._storename
    
    @storename.setter
    def storename(self, storename):
        self._storename = storename

    def add_item(self):
        #Display addable items
        print("-----------------------------------------------\n" +
              "|               \033[1mADDABLE ITEMS\033[0m                 |\n"
            + tabulate.tabulate(items_addable_table, headers="keys", tablefmt="fancy_grid")
             )
        #Adding logic
        while True:
            try:
                item_input = str(input("Enter item to add(/b for back): ")).strip().lower()
                if item_input != "/b":
                    item_input = item_input.capitalize()
                elif item_input == "/b":
                    break
            except (ValueError, EOFError):
                continue
            # Check item exists
            item_exists = False
            with open(f"csvs\\{self._storename}_data.csv") as user_file:
                file_items = csv.DictReader(user_file)
                for row in file_items:
                    if item_input == row["item_name"]:
                        item_exists = True
                        break
                if item_exists:
                    print("--------------------\n\033[91m\033[1mItem Already Exists\033[0m\033[0m\n--------------------")
                    continue
                elif item_input not in items_addable_table["Item"]:
                    print("--------------\n\033[91m\033[1mItem Not Found\033[0m\033[0m\n--------------")
                    continue
                # Add item
                elif item_input in items_addable_table["Item"]:
                    cost = np.float64(items_addable_prices[item_input])
                    if self.no_budget(cost, nocall = False):
                        break
                    self.update_budget_subtract(cost)        
                    self.update_profit(-cost)
                    self.update_leaderboard_budget()
                    with open(f"csvs\\{self._storename}_data.csv", "a", newline="") as user_itemsfile:
                        items_writer = csv.DictWriter(user_itemsfile, fieldnames=["item_name","quantity","price","profit","budget"])
                        items_writer.writerow({"item_name": item_input, "quantity": 100, "price": set_price(item_input), "profit": row["profit"], "budget": row["budget"]})
                        print(f"\033[92m\033[1mItem '{item_input}' added successfully\033[0m\033[0m")
                else:
                    print("--------------\n\033[91m\033[1mItem Not Found\033[0m\033[0m\n--------------")
                    continue

    def delete_item(self):
        # Display Items
        with open(f"csvs\\{self._storename}_data.csv") as file:
                reader = csv.DictReader(file)
                items = list(reader)
 
                # Filter out the first row (default values) and any rows with all empty values for specific fields
                valid_items = [
                    row for row in items if row['item_name'] or row['quantity'] or row['price']
                ]
                # Extract only the relevant fields
                display_items = [
                    {'item_name': row['item_name'], 'quantity': row['quantity'], 'price': row['price']}
                    for row in valid_items
                ]
                if not display_items:
                    print("-----------------\n\033[91m\033[1mNo items in store\033[0m\033[0m\n-----------------")
                    return
                else:
                    print(f"--------------------------------------\n|           \033[1mCURRENT ITEMS\033[0m            |\n{tabulate.tabulate(display_items, headers="keys", tablefmt="fancy_grid")}")

        #Deleting logic
        while True:
            try:
                item_to_delete = str(input("Enter item to delete(/b for back): ")).lower().strip()
                if item_to_delete == "/b":
                    break
                if not item_to_delete:
                    print("--------------\n\033[91m\033[1mItem Not Found\033[0m\033[0m\n--------------")
                    continue
                item_to_delete = item_to_delete.capitalize()
            except (ValueError, EOFError):
                continue 
            
            # Confirmation

            item_found = False
            updated_items = []
            for row in items:
                if row["item_name"] == item_to_delete:
                    item_found = True
                else:
                    updated_items.append(row)
            
            if not item_found:
                print("--------------\n\033[91m\033[1mItem Not Found\033[0m\033[0m\n--------------")
                continue
            
            # Update the items list (only adds the items which did not match user input)
            else:
                try:
                    confirm = str(input("Continue? Items are non refundable(Y/N): ")).lower().strip()
                    if confirm == "n":
                        break
                    elif confirm == "y":
                        # Update the items list (only adds the items which did not match user input)
                        items = updated_items
                        # Write the updated list back to the CSV file
                        with open(f"csvs\\{self._storename}_data.csv", mode='w', newline='') as file_rewrite:
                            writer = csv.DictWriter(file_rewrite, fieldnames=["item_name", "quantity", "price", "profit", "budget"])
                            writer.writeheader()
                            writer.writerows(updated_items)
                            print(f"\033[92m\033[1mItem '{item_to_delete}' deleted successfully\033[0m\033[0m")
                except (ValueError, EOFError):
                    continue

    def change_price(self):
        with open(f"csvs\\{self._storename}_data.csv") as file:
                reader = csv.DictReader(file)
                items = list(reader)
 
                # Filter out the first row (default values) and any rows with all empty values for specific fields
                valid_items = [
                    row for row in items if row['item_name'] or row['quantity'] or row['price']
                ]
                # Extract only the relevant fields
                display_items = [
                    {'item_name': row['item_name'], 'quantity': row['quantity'], 'price': row['price']}
                    for row in valid_items
                ]
                if not display_items:
                    print("-----------------\n\033[91m\033[1mNo items in store\033[0m\033[0m\n-----------------")
                    return
                else:
                    print(f"--------------------------------------\n|           \033[1mCURRENT ITEMS\033[0m            |\n{tabulate.tabulate(display_items, headers="keys", tablefmt="fancy_grid")}")
 
        while True:
            try:
                item_to_change = str(input("Enter item to change(/b for back): ")).lower().strip()
                if item_to_change == "/b":
                    break
                if not item_to_change:
                    print("--------------\n\033[91m\033[1mItem Not Found\033[0m\033[0m\n--------------")
                    continue
                item_to_change = item_to_change.capitalize()
            except (ValueError, EOFError):
                continue 

            item_found = False
            updated_items = []
            
            for row in items:
                if row["item_name"] == item_to_change:
                    quantity = row["quantity"]
                    item_found = True
                else:
                    updated_items.append(row)
            
            if not item_found:
                print("--------------\n\033[91m\033[1mItem Not Found\033[0m\033[0m\n--------------")
                continue
            else:
                new_price = set_price(item_to_change)
                changed_dict = {"item_name": item_to_change, "quantity": quantity, "price": new_price, "profit": row["profit"], "budget": row["budget"]}
                updated_items.append(changed_dict)
                items = updated_items

            with open(f"csvs\\{self._storename}_data.csv", mode='w', newline='') as file_rewrite:
                file_rewriter = csv.DictWriter(file_rewrite, fieldnames=["item_name", "quantity", "price", "profit", "budget"])
                file_rewriter.writeheader()
                file_rewriter.writerows(updated_items)

    def restock(self):
        # Display Items
        with open(f"csvs\\{self._storename}_data.csv") as file:
                reader = csv.DictReader(file)
                items = list(reader)
 
                # Filter out the first row (default values) and any rows with all empty values for specific fields
                valid_items = [
                    row for row in items if row['item_name'] or row['quantity'] or row['price']
                ]
                # Extract only the relevant fields
                display_items = [
                    {'item_name': row['item_name'], 'quantity': row['quantity'], 'price': row['price']}
                    for row in valid_items
                ]
                if not display_items:
                    print("-----------------\n\033[91m\033[1mNo items in store\033[0m\033[0m\n-----------------")
                    return
                else:
                    print(f"--------------------------------------\n|           \033[1mCURRENT ITEMS\033[0m            |\n{tabulate.tabulate(display_items, headers="keys", tablefmt="fancy_grid")}")
                    
        while True:
            try:
                item_to_restock = str(input("Enter item to restock(/b for back): ")).lower().strip()
                if item_to_restock == "/b":
                    break
                item_to_restock = item_to_restock.capitalize()
            except (ValueError, EOFError):
                continue 
            if not item_to_restock:
                print("--------------\n\033[91m\033[1mItem Not Found\033[0m\033[0m\n--------------")
                continue

            item_found = False
            updated_items = []
            
            for row in items:
                if row["item_name"] == item_to_restock:
                    quantity = int(row["quantity"])
                    price_per_unit = np.float64(items_addable_prices[item_to_restock]/100)
                    item_found = True
                else:
                    updated_items.append(row)
            
            if not item_found:
                print("--------------\n\033[91m\033[1mItem Not Found\033[0m\033[0m\n--------------")
                continue
            else:
                new_quantity = 100
                cost = np.float64((new_quantity - quantity) * price_per_unit)
                if self.no_budget(cost, nocall = False):
                    break
                changed_dict = {"item_name": item_to_restock, "quantity": new_quantity, "price": row["price"], "profit": row["profit"], "budget": row["budget"]}
                updated_items.append(changed_dict)
                items = updated_items
                with open(f"csvs\\{self._storename}_data.csv", mode='w', newline='') as file_rewrite:
                    file_rewriter = csv.DictWriter(file_rewrite, fieldnames=["item_name", "quantity", "price", "profit", "budget"])
                    file_rewriter.writeheader()
                    file_rewriter.writerows(updated_items)
                    print(f"\033[92m\033[1mItem '{item_to_restock}' restocked successfully\033[0m\033[0m")
                self.update_budget_subtract(cost)
                self.update_profit(-cost)
                self.update_leaderboard_budget()
                
    def exit(self):
        sys.exit(bold("Goodbye!"))

    def help(self):
        print(tabulate.tabulate(help_table, headers="keys", tablefmt="fancy_grid"))

    def delete_store(self):
        self.update_passwords_delete()
        self.update_leaderboard_delete()
        os.remove(f"csvs\\{self._storename}_data.csv")
        sys.exit(bold(f"\033[91m'{self._storename}' has been deleted\033[0m"))

    def view_profit(self, nocall = False):
        with open(f"csvs\\{self._storename}_data.csv") as file:
            reader = csv.DictReader(file)
            items = list(reader)
            for row in items:
                if not nocall:
                    print(f"Profit: {row["profit"]}")
                return np.float64(row["profit"]) 
 
    def view_budget(self, nocall= False):
        with open(f"csvs\\{self._storename}_data.csv") as file:
            reader = csv.DictReader(file)
            items = reader
            for row in items:
                if not nocall:
                    print(f"Budget: {row["budget"]}")
                return np.float64((row["budget"]))
                
    def view_items(self, nocall = False):
        with open(f"csvs\\{self._storename}_data.csv") as file:
                reader = csv.DictReader(file)
                items = list(reader)
 
                # Filter out the first row (default values) and any rows with all empty values for specific fields
                valid_items = [
                    row for row in items if row['item_name'] or row['quantity'] or row['price']
                ]
                # Extract only the relevant fields
                display_items = [
                    {'item_name': row['item_name'], 'quantity': row['quantity'], 'price': row['price']}
                    for row in valid_items
                ]
                if not nocall:
                    if not display_items:
                        print("-----------------\n\033[91m\033[1mNo items in store\033[0m\033[0m\n-----------------")
                        return False
                    else:
                        print(f"--------------------------------------\n|           \033[1mCURRENT ITEMS\033[0m            |\n{tabulate.tabulate(display_items, headers="keys", tablefmt="fancy_grid")}")
                        return items

    def view_leaderboard(self):
        with open("csvs\\leaderboard.csv", newline="") as file:
            reader = csv.DictReader(file)
            leaderboard_data = list(reader)
        
        # Sort data based on 'budget' in descending order
        sorted_data = sorted(leaderboard_data, key=lambda x: np.float64(x['budget']), reverse=True)
        if not sorted_data:
                    print("----------------\n\033[91m\033[1mNo users to show\033[0m\033[0m\n----------------")
                    return
        else:
            # Prepare table headers and rows for tabulate
            headers = ['Rank', 'Store Name', 'Budget']
            rows = [[rank + 1, row['storename'], row['budget']] for rank, row in enumerate(sorted_data)]
            # Generate the table using tabulate
            table = tabulate.tabulate(rows, headers=headers, tablefmt="fancy_grid", )
            print(table)

    def update_budget_subtract(self, cost):
        current_budget = np.float64(self.view_budget(nocall=True))
        new_budget = current_budget - np.float64(cost)
        
        # Update the first row of the CSV file
        with open(f"csvs\\{self._storename}_data.csv", newline='') as file_read:
            reader = csv.DictReader(file_read)
            rows = list(reader)  # Convert to list to modify
            
            if rows:
                rows[0]['budget'] = np.float64(new_budget)  # Update the budget in the first row
            
            # Write the updated rows back to the CSV file
            with open(f"csvs\\{self._storename}_data.csv", "w", newline='') as file_write:
                fieldnames = ['item_name', 'quantity', 'price', 'profit', 'budget']
                writer = csv.DictWriter(file_write, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

    def update_profit(self, profit):
        current_profit = np.float64(self.view_profit(nocall =True))
        new_profit = current_profit + np.float64(profit)

        with open(f"csvs\\{self._storename}_data.csv", newline='') as file_read:
            reader = csv.DictReader(file_read)
            rows = list(reader)  # Convert to list to modify
            
            if rows:
                rows[0]['profit'] = np.float64(new_profit)  # Update the budget in the first row
            
            # Write the updated rows back to the CSV file
            with open(f"csvs\\{self._storename}_data.csv", "w", newline='') as file_write:
                fieldnames = ['item_name', 'quantity', 'price', 'profit', 'budget']
                writer = csv.DictWriter(file_write, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

    def update_passwords_delete(self):
        with open("csvs\\passwords.csv") as file:
                reader = csv.DictReader(file)
                items = list(reader)

        updated_items = []
        store_found = False
        for row in items:
            if row["storename"] == self._storename:
                store_found = True
            else:
                updated_items.append(row)
        
        if store_found:
            items = updated_items

        with open("csvs\\passwords.csv", mode='w', newline='') as file_rewrite:
            file_rewriter = csv.DictWriter(file_rewrite, fieldnames=['storename', 'password'])
            file_rewriter.writeheader()
            file_rewriter.writerows(updated_items)
    
    def update_leaderboard_delete(self):
        with open("csvs\\leaderboard.csv") as file:
                reader = csv.DictReader(file)
                items = list(reader)

        updated_items = []
        store_found = False
        for row in items:
            if row["storename"] == self._storename:
                store_found = True
            else:
                updated_items.append(row)
        
        if store_found:
            items = updated_items

        with open("csvs\\leaderboard.csv", mode='w', newline='') as file_rewrite:
            file_rewriter = csv.DictWriter(file_rewrite, fieldnames=['storename', 'budget'])
            file_rewriter.writeheader()
            file_rewriter.writerows(updated_items)

    def no_budget(self, cost, nocall = False):
        budget = np.float64(self.view_budget(nocall=True))
        if cost > budget:
            if not nocall:    
                print(bold("\033[91mNot Enough Budget\033[0m"))
            return True
        return False

    def check_bankrupt(self):
        budget = np.float64(self.view_budget(nocall=True))
        if budget < 20 and (self.view_items(nocall=True) == False or self.check_quantities()):
            print("\033[91m------------------------\nTHE STORE WENT BANKRUPT!\n------------------------\033[0m")
            return True
        else: return False
    
    def check_quantities(self):
        with open(f"csvs\\{self._storename}_data.csv") as file:
            reader = csv.DictReader(file)
            quantities = [int(row['quantity']) for row in reader if row['item_name']]  # Ensure item_name is not empty
        return all(quantity < 1 for quantity in quantities)

    def update_leaderboard_budget(self):
        with open("csvs\\leaderboard.csv") as file:
                reader = csv.DictReader(file)
                items = list(reader)

        updated_items = []
        store_found = False
        budget = np.float64(self.view_budget(nocall= True))
        for row in items:
            if row["storename"] == self._storename:
                store_found = True
            else:
                updated_items.append(row)
        
        if store_found:
            changed_dict = {"storename": self._storename,"budget": budget}
            updated_items.append(changed_dict)
            items = updated_items

        with open("csvs\\leaderboard.csv", mode='w', newline='') as file_rewrite:
            file_rewriter = csv.DictWriter(file_rewrite, fieldnames=['storename', 'budget'])
            file_rewriter.writeheader()
            file_rewriter.writerows(updated_items)


class Customer(Owner):
    def __init__(self, action: str = None, storename=None):
        super().__init__(action, storename)
    
    def buy_items(self):
        # Display Items
        with open(f"csvs\\{self._storename}_data.csv") as file:
                reader = csv.DictReader(file)
                items = list(reader)
 
                # Filter out the first row (default values) and any rows with all empty values for specific fields
                valid_items = [
                    row for row in items if row['item_name'] or row['quantity'] or row['price']
                ]
                # Extract only the relevant fields
                display_items = [
                    {'item_name': row['item_name'], 'quantity': row['quantity'], 'price': row['price']}
                    for row in valid_items
                ]
                if not display_items:
                    print("-----------------\n\033[91m\033[1mNo items in store\033[0m\033[0m\n-----------------")
                    return 
                else:
                    print(f"--------------------------------------\n|           \033[1mCURRENT ITEMS\033[0m            |\n{tabulate.tabulate(display_items, headers="keys", tablefmt="fancy_grid")}")

        while True:
            try:
                item_buy = str(input("Enter item to buy(/b for back): ")).strip().lower()
                if item_buy == "/b":
                    break
                if not item_buy:
                    print("--------------\n\033[91m\033[1mItem Not Found\033[0m\033[0m\n--------------")
                    continue
                item_buy = item_buy.capitalize()
            except (ValueError, EOFError):
                continue
            item_found = False
            updated_items = []
            for row in items:
                if row["item_name"] == item_buy:
                    price = np.float64(row["price"])
                    quantity = int(row["quantity"])
                    item_found = True
                else:
                    updated_items.append(row)
            
            if not item_found:
                print("--------------\n\033[91m\033[1mItem Not Found\033[0m\033[0m\n--------------")
                continue
            else:
                if quantity < 1:
                    print(f"--------------\n\033[91m\033[1m'{item_buy} is no longer in stock'\033[0m\033[0m\n--------------")
                    break
                new_quantity = int(quantity - 1) 
                cost_price = np.float64(items_addable_prices[item_buy]/100)
                earnings = np.float64(np.float64(price) - cost_price)
                changed_dict = {"item_name": item_buy, "quantity": new_quantity, "price": price, "profit": row["profit"], "budget": row["budget"]}
                updated_items.append(changed_dict)
                items = updated_items
                with open(f"csvs\\{self._storename}_data.csv", mode='w', newline='') as file_rewrite:
                    file_rewriter = csv.DictWriter(file_rewrite, fieldnames=["item_name", "quantity", "price", "profit", "budget"])
                    file_rewriter.writeheader()
                    file_rewriter.writerows(updated_items)
                self.update_budget_subtract(-earnings)
                self.update_profit(earnings)
                self.update_leaderboard_budget()
                print(f"\033[92m\033[1mItem '{item_buy}' bought successfully\033[0m\033[0m")

    def review(self):
        budget = np.float64(self.view_budget(nocall=True))
        review_option = questionary.select(
        "How was your experience?",
        choices=[
            "Good",
            "It Was Ok",
            "Bad",
            "Very Bad",
            "I Hated It"
        ]).ask()
        match review_option:
            case "Good":
                budget_addition = np.float64(np.float64(budget) * 1/100)
                self.update_budget_subtract(-budget_addition)
                self.update_profit(budget_addition)
                print("\033[92m\033[1mThank You for your Feedback\033[0m\033[0m")
            case "It Was Ok":
                print("\033[92m\033[1mThank You for your Feedback\033[0m\033[0m")
            case "Bad":
                budget_deduction = np.float64(np.float64(budget) * 1/100)
                self.update_budget_subtract(budget_deduction)
                self.update_profit(-budget_deduction)
                print("\033[92m\033[1mThank You for your Feedback\033[0m\033[0m")
            case "Very Bad":
                budget_deduction = np.float64(np.float64(budget) * 2.5/100)
                self.update_budget_subtract(budget_deduction)
                self.update_profit(-budget_deduction)
                print("\033[92m\033[1mThank You for your Feedback\033[0m\033[0m")
            case "I Hated It":
                budget_deduction = np.float64(np.float64(budget) * 5/100)
                self.update_budget_subtract(budget_deduction)
                self.update_profit(-budget_deduction)
                print("\033[92m\033[1mThank You for your Feedback\033[0m\033[0m")
        self.update_leaderboard_budget()
            
    def customer_help(self):
        print(tabulate.tabulate(help_table_customer, headers="keys", tablefmt="fancy_grid"))
