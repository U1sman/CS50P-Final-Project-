# PYTHON GROCERY STORE
### Video Demo:  <https://www.youtube.com/watch?v=vx1BI4g55zg>
## Description
This project called **PYTHON GROCERY STORE**, is a **CLI**<sup> (Command Line Interface)</sup> based simulation of a grocery store.

It contains the roles **Owner** and **Customer**.

On Startup using the command **"python project.py"** the user can select between the two roles, **Owner** and **Customer**.

- If the **Owner** role is selected, the program will ask the user to either **"Log Into Existing Store"** , **"Create New Store"** or **"Exit"**.

    - If the **"Log Into Existing Store"** option is selected, it will ask the user for a "storename" and then a "password" for that store, if the store does not exist or the password is wrong, the program will display an error message and reprompt the user but if it is right the user will be logged into the store. The "storename" and "password" prompts are accompanied by an option to type "/e" which will exit the program

    - If the **"Create New Store"** option is selected, it will also ask the user for a "storename" and then a "password" for a store. If the storename does not match the name of an existing store, It will create the store, else if a store if the same name does exist, the program will display an error message and reprompt the user. The "storename" and "password" prompts are accompanied by an option to type "/e" which will exit the program

    - If the **"Exit"** option is selected, it will exit the program itself.

- If the **Customer** role is selected, the program will put the user into a random store where they can perform their functionalities.

Once logged in either as the **Owner** or **Customer**, the program will ask the user to type a valid Action, if not valid an error message will be displayed followed by a reprompt. This part of the program will be referred to as "start".

Both the **Owner** and **Customer** can perform certain Actions.

#### **Owner Actions:**

1. View Items

        Displays the item_names, quantities and the price from the {storename}_data.csv file in a table using tabulate, If the item_name column is found to be empty then the program will print that there are no items in the store.
2. View Budget

        Displays the budget of the store/owner from the {storename}_data.csv file
3. View Profit

        Displays the profit of the store/owner from the {storename}_data.csv file
4. View Leaderboard

        Displays the users from the leaderboard.csv file in descending order based on their budget in a table using tabulate
5. Add Item 

        This First displays the addable items (i.e items that can be added into the store) in the form of a table using tabulate and then gives you the option to either add an item to the store or type /b and go back to "start". If a valid item from the addable items that does not already exist in the {storename}_data.csv file is inputted, the program will then ask the owner to set the price for that item also displaying the cost per unit, once the price has been set, the cost of 100 units of that item will be subtracted from the budget and profit and then the item_name, quantity(which is 100) and price will be written to the {storename}_data.csv file else the program will display an error message and reprompt the user. Also, if the user tries to add an item and they don't have the budget for it, it will display an error.
6. Delete Item

        This Fist displays the Current items in the store in form of a table using tabulate from the {storename}_data.csv file. It then prompts the user to input a valid item from the current items or type /b and go back to "start" and then deletes the row with the matching item name, the cost for that item is not refunded so before deleting the item, the user is prompted whether they want to delete the item or not and then the rest will happen based on their input. If an invalid input is given in both of these prompts, the program will display an error message and reprompt the user.
7. Change Price

        This Fist displays the Current items in the store in form of a table using tabulate from the {storename}_data.csv file. It then prompts the user to input a valid item from the current items or type /b and go back to "start" and then prompts them for a new price, once this is done, the updated data will be written back to the {storename}_data.csv file. If an invalid input is given in both of these prompts, the program will display an error message and reprompt the user.
8. Restock

        This Fist displays the Current items in the store in form of a table using tabulate from the {storename}_data.csv file. It then prompts the user to input a valid item from the current or items type /b and go back to "start" and then it restores the quantity back to 100 also subtracting the cost for this from both the profit and budget. If an invalid input is given in this prompt, the program will display an error message and reprompt the user. Also, if the user tries to restock an item and they don't have the budget for it, it will display an error.
9. Help

        Displays the valid Actions for the Owner in a table using tabulate.
10. Exit

        This uses sys.exit() to exit the program.
11. Delete Store

        This deletes all the information related to the user from the leaderboard.csv file, passwords.csv file and deletes the {storename}_data.csv file of the specific user.

- Check Bankrupt(Extra Functionality)

        This checks whether the owner went bankrupt on each action. The way it works is it calls the check_bankrupt method on initialization of the Owner class to check whether the store went bankrupt, if True, the user is deleted along with a message alerting that the store went bankrupt. The method checks the {storename}_data.csv file to see if the Owner's/Store's budget is below 20 and if one of these is true: there are no items in the {storename}_data.csv file or the quantity of all the items is below 1

#### **Customer Actions:**

1. View Items

        Displays the item_names, quantities and the price from the {storename}_data.csv file in a table using tabulate, If the item_name column is found to be empty then the program will print that there are no items in the store.
2. Buy Items

        This Fist displays the Current items in the store in form of a table using tabulate from the {storename}_data.csv file. It then prompts the user to input a valid item from the current items or type /b and go back to "start" and then first reduces the quantity by one, then adds the profit made from the item to the budget and profit of the owner/store. If an invalid input is given in this prompt, the program will display an error message and reprompt the user. Also, if the customer tries to buy an item and no quantity is left it will display an error.
3. Review

        This is a way to give feedback to the owner of the store. It will provide you with 5 options of reviews to choose from based on your preference using questionary, the options are "Good","It Was Ok","Bad","Very Bad","I Hated It", each of these options has a percentage ranging from 0-5% which is the amount that will either be added or deducted from the owner's/store's budget and profit.
4. Help

        Displays the valid Actions for the Customer in a table using tabulate.
5. Exit

        This uses sys.exit() to exit the program.

This program is seperated into three files, **project.py**, **passwords.py** and **roles.py**, these files contain all the code for the program. There is another folder that comes with them called **csvs** containing "leaderboard.csv","passwords.csv" and "{storename}_data.csv".

These are the functions of each code file the it program:

### **project.py**
1. main

        Choose between Owner and Customer using tabulate
2. owner

        Calls the passwords.password function from passwords.py

        Gets user input for the Action

        Creates an instance for the Owner class from roles.py
3. customer

        Gets a random storename

        Gets user input for the Action

        Creates an instance for the Customer class from roles.py
4. owner_action

        Validates the user input from the owner function
5. customer_action

        Validates the user input from the  function
6. random_store

        Fetches a random storename from the passwords.py file

### **passwords.py**

1. password

        Asks the user to choose between loging in, signing up or exiting the program and calls a function accordingly

2. login

        Asks for the storename and password of the store and has the option of exiting the program with it

        It also calls the login_authenticator function aswell 

3. signup 

        Asks for the storename and password of the store and has the option of exiting the program with it

        Calls the signup_authenticator function

        Calls the create_item_file function and calls the create_leaderboard function aswell

4. login_authenticator

        Returns True or False based on the validity of the storename and the password

5. signup_authenticator

        Returns True or False based on the validity of the storename and the password

6. create_item_file

        Creates the {storename}_data.csv file for the specific store

7. create_leaderboard

        Adds the storename aswell as the budget into the leaderboard.csv file 

### **roles.py**

Contains the **Owner** and **Customer** and some functions such as "bold" and "set_price"

Both classes contain the methods that can be performed onto or by the role and the functionalities related to both roles
