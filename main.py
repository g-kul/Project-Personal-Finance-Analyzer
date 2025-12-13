from datetime import datetime
import json
import os



# global variables
all_transactions_list = []
save_all_transactions_list = []
budgets = {}
save_budgets = {}


# Main menu function
def main_menu():
    menu = [
        "Add Transaction",
        "View all transaction",
        "View Transactions by Category",
        "View Summary & Statistics",
        "Set Budget for Category",
        "Check Budget Status",
        "Generate Monthly Report",
        "Exit",
    ]
    i = 1
    for n in menu:
        print(i, ". ", n)
        i += 1


def user_menu_input():
    try:
        user_input = int(input("Enter your choice: "))
    except:
        user_input = -1
    return user_input
    # if else to check entry


def get_datetime_input():
    while True:
        date_str = input('Enter the date in "dd/mm/yyyy" format: ')
        try:
            date_formatted = datetime.strptime(date_str, "%d/%m/%Y")
            return date_formatted
        except:
            print("Enter a valid date in the specified format")


def get_month():
    while True:
        month_str = input('Enter the month in "mm/yyyy" format: ')
        try:
            month_formatted = datetime.strptime(month_str, "%m/%Y")
            return month_formatted
        except:
            print("Enter a valid month in the specified format")


def add_transactions():
    global all_transactions_list
    while True:
        entry = []
        try:
            choice = int(input("Enter 0 to exit or 1 to enter a transaction data"))
        except:
            choice = -1
        if choice == 1:
            print(
                "Enter your transactions below, it follows the format Transaction = (date, transaction type, amount, category, description)"
            )
            date = get_datetime_input()
            t_type = int(
                input(
                    "Enter the type of transaction: \n\n1.Enter 1 for income\n2.Enter 2 for expense"
                )
            )
            if t_type == 1:
                transaction_type = "income"
                ctgry = 1
            elif t_type == 2:
                transaction_type = "expense"
                ctgry = 2
            if ctgry == 1:
                inc_ctgry = int(
                    input(
                        "Enter the type of income: \n\n1. Enter 1 for salary 2. Enter 2 for others"
                    )
                )
                if inc_ctgry == 1:
                    category = "salary"
                elif inc_ctgry == 2:
                    category = "others"
            elif ctgry == 2:
                exp_ctgry = int(
                    input(
                        "Enter the type of expense: \n\n\
                                1. Enter 1 for Food\n\
                                2. Enter 2 for Entertainment\n\
                                3. Enter 3 for Travel\n\
                                4. Enter 4 for Personal\n\
                                5. Enter 5 for Miscellaneuos"
                    )
                )
                if exp_ctgry == 1:
                    category = "Food"
                elif exp_ctgry == 2:
                    category = "Entertainment"
                elif exp_ctgry == 3:
                    category = "Travel"
                elif exp_ctgry == 4:
                    category = "Personal"
                elif exp_ctgry == 5:
                    category = "Miscellaneuos"
            amount = float(input("Enter the amount of transaction: "))
            expense_description = input("Enter the description for your transaction: ")
            entry = [
                date,
                transaction_type,
                amount,
                category,
                expense_description,
            ]
            if budgets != {}:
                for dte in budgets:
                    if dte.month == entry[0].month and dte.year == entry[0].year:
                        sum = 0
                        for i in all_transactions_list:
                            if i[3] == entry[3]:
                                sum += i[2]
                        sum += entry[2]
                        if sum > budgets[dte][entry[3]]:
                            print(
                                f"You will go over budget for category {entry[3]} for month {entry[0].month}"
                            )
                            option = int(
                                input(
                                    (
                                        "Do you want to still continue with adding this and editing monthly budget press 1 OR enter 0 to cancel this entry"
                                    )
                                )
                            )
                            if option == 1:
                                result = tuple(entry)
                                all_transactions_list.append(result)
                                global budgets
                                set_budget()
                            elif option == 2:
                                break
                        else:
                            result = tuple(entry)
                            all_transactions_list.append(result)
            elif budgets == {}:
                result = tuple(entry)
                all_transactions_list.append(result)
        elif choice == 0:
            break
        elif choice not in {0, 1} or choice == -1:
            print("Enter a valid choice!!!")

    # iterate through entry and enter into list with sublist for each entry


def view_transactions():
    choice = int(input("Enter the transcations you wish to view: \nEnter 1 to view all transactions you have entered so far\n \
                        Enter 2 to view transcations by month\n \
                        or Enter 3 to show transactions for a range of dates you have entered"))
    if choice == 1:
        if all_transactions_list == []:
            print("You havent entered any transcations yet!")
        else:
            n = 1
            for i in all_transactions_list:
                print("Each transaction done by you are:  ")
                print(n, ". ", i)
                n += 1
    elif choice == 2:
        month_option = get_month()
        a = 1
        for i in all_transactions_list:
            if i[0].month == month_option.month and i[0].year == month_option.year:
                print(a,". ",i)
                a += 1
    elif choice == 3:
        start_date = get_datetime_input()
        end_date = get_datetime_input()
        found = False
        b = 1
        for i in all_transactions_list:
            if start_date == end_date and i[0] == start_date:
                print(b,". ",i)
                found = True
            elif i[0] >= start_date and i[0] <= end_date:
                print(b,". ",i)
                found = True
        if not found:
            print("There are no entires entered for the selected dates!")
    else:
        print("Please enter a valid choice!!!")




def view_transactions_category():
    choice = int(
        input(
            "Enter the type of transaction you wish to see\n\n\
                    1. Enter 1 for seeing those under income\n\
                    2. Enter 2 for seeing those under expense\n"
        )
    )
    if choice == 1:
        ttype = "income"
        options = int(
            input(
                "Enter the choice of transaction in income: \n\n\
                         Enter 1 for seeing under 'salary'\n\
                         Enter 2 for seeing under 'others'\n"
            )
        )
        if options == 1:
            category = "salary"
        elif options == 2:
            category = "others"
    elif choice == 2:
        ttype = "expense"
        options = int(
            input(
                "Enter the choice of transaction in expense: \n\n\
                        1. Enter 1 seeing under Food\n\
                        2. Enter 2 seeing under Entertainment\n\
                        3. Enter 3 seeing under Travel\n\
                        4. Enter 4 seeing under Personal\n\
                        5. Enter 5 seeing under Miscellaneuos"
            )
        )
        if options == 1:
            category = "Food"
        elif options == 2:
            category = "Entertainment"
        elif options == 3:
            category = "Travel"
        elif options == 4:
            category = "Personal"
        elif options == 5:
            category = "Miscellaneuos"
    else:
        print("Please enter a valid choice!!!")
    month_choice = get_month()
    print(f"Your selected transactions for the month {month_choice.month} in {month_choice.year}are: \n\n")
    found = False
    n = 0
    for i in all_transactions_list:
        if (i[1] == ttype and i[3] == category) and (i[0].month == month_choice.month and i[0].year == month_choice.year):
            print("Index: ", n, " ", i)
            found = True
        n += 1
    if not found:
        print("No entry has been found!")


def summary():
    income = 0
    expense = 0
    salary = 0
    others = 0
    Food = 0
    Entertainment = 0
    Travel = 0
    Personal = 0
    Miscellaneuos = 0
    choice = int(input("Enter the choice of viewing your transactions summary\nEnter 1 for viewing entire summary\nEnter 2 for viewing summary for month of choice: "))
    if choice == 1:
        print("The summary of your entire transactions are:  ")
        for i in all_transactions_list:
            if i[1] == "income" and i[3] == "salary":
                income += i[2]
                salary += i[2]
            elif i[1] == "income" and i[3] == "others":
                income += i[2]
                others += i[2]
            elif i[1] == "expense" and i[3] == "Food":
                expense += i[2]
                Food += i[2]
            elif i[1] == "expense" and i[3] == "Entertainment":
                expense += i[2]
                Entertainment += i[2]
            elif i[1] == "expense" and i[3] == "Travel":
                expense += i[2]
                Travel += i[2]
            elif i[1] == "expense" and i[3] == "Personal":
                expense += i[2]
                Personal += i[2]
            elif i[1] == "expense" and i[3] == "Miscellaneuos":
                expense += i[2]
                Miscellaneuos += i[2]

        print(
            "The summary of your transactions are: \n\n",
            f"Income: {income}\n",
            f"Salary: {salary}\n",
            f"Other_income: {others}\n",
            f"Expense: {expense}\n",
            f"Food: {Food}\n",
            f"Entertainment: {Entertainment}\n",
            f"Travel: {Travel}\n",
            f"Personal: {Personal}\n",
            f"Miscellaneuos: {Miscellaneuos}\n",
        )
    elif choice == 2:
        summary_month = get_month()
        print("The summary of your entire transactions are:  ")
        for i in all_transactions_list:
            if i[0].month == summary_month.month and i[0].year == summary_month.year:
                if i[1] == "income" and i[3] == "salary":
                    income += i[2]
                    salary += i[2]
                elif i[1] == "income" and i[3] == "others":
                    income += i[2]
                    others += i[2]
                elif i[1] == "expense" and i[3] == "Food":
                    expense += i[2]
                    Food += i[2]
                elif i[1] == "expense" and i[3] == "Entertainment":
                    expense += i[2]
                    Entertainment += i[2]
                elif i[1] == "expense" and i[3] == "Travel":
                    expense += i[2]
                    Travel += i[2]
                elif i[1] == "expense" and i[3] == "Personal":
                    expense += i[2]
                    Personal += i[2]
                elif i[1] == "expense" and i[3] == "Miscellaneuos":
                    expense += i[2]
                    Miscellaneuos += i[2]
        print(
            f"The summary of your transactions for the month {summary_month.month} of year {summary_month.year} are: \n\n",
            f"Income: {income}\n",
            f"Salary: {salary}\n",
            f"Other_income: {others}\n",
            f"Expense: {expense}\n",
            f"Food: {Food}\n",
            f"Entertainment: {Entertainment}\n",
            f"Travel: {Travel}\n",
            f"Personal: {Personal}\n",
            f"Miscellaneuos: {Miscellaneuos}\n",
        )



def set_budget():
    global budgets
    print("Enter the month for which you wish to set the budget below")
    budget_month = get_month()
    Food_budget = float(input("Enter the budget for food: "))
    Entertainment_budget = float(input("Enter the budget for Entertainment: "))
    Travel_budget = float(input("Enter the budget for Travel: "))
    Personal_budget = float(input("Enter the budget for Personal: "))
    Miscellaneous_budget = float(input("Enter the budget for Miscellaneous: "))
    budget_targets = {
        "Food": Food_budget,
        "Entertainment": Entertainment_budget,
        "Travel": Travel_budget,
        "Personal": Personal_budget,
        "Miscellaneuos": Miscellaneous_budget,
    }
    budgets[budget_month] = budget_targets


def budget_status():
    status_month = get_month()
    income = 0
    expense = 0
    salary = 0
    others = 0
    Food = 0
    Entertainment = 0
    Travel = 0
    Personal = 0
    Miscellaneuos = 0
    list_of_items = []
    for i in all_transactions_list:
        if i[0].month == status_month.month and i[0].year == status_month.year:
            if i[1] == "income" and i[3] == "salary":
                income += i[2]
                salary += i[2]
            elif i[1] == "income" and i[3] == "others":
                income += i[2]
                others += i[2]
            elif i[1] == "expense" and i[3] == "Food":
                expense += i[2]
                Food += i[2]
            elif i[1] == "expense" and i[3] == "Entertainment":
                expense += i[2]
                Entertainment += i[2]
            elif i[1] == "expense" and i[3] == "Travel":
                expense += i[2]
                Travel += i[2]
            elif i[1] == "expense" and i[3] == "Personal":
                expense += i[2]
                Personal += i[2]
            elif i[1] == "expense" and i[3] == "Miscellaneuos":
                expense += i[2]
                Miscellaneuos += i[2]
    for i,j in budgets.items():
        if i.month == status_month.month and i.year == status_month.year:
            for key,values in j.items():
                list_of_items.append(values)
    if list_of_items:
        expense_budget_total = sum(list_of_items)
    else:
        expense_budget_total = 0
    print(
        f"The budget status of your transactions for the month {status_month.month} of year {status_month.year} are: \n\n",
        f"Total Income for the month: {income}\n",
        f"Salary for the month: {salary}\n",
        f"Other_income for the month: {others}\n",
        f"Expense for the month: {expense} and budget for expense for month {expense_budget_total}\n",
        f"Food expense for the month is: {Food} and budget for Food for month is {budgets[status_month]["Food"]}\n",
        f"Entertainment for the month is: {Entertainment} and budget for Entertainment for the month is {budgets[status_month]["Entertainment"]}\n",
        f"Travel for the month is: {Travel} and budget for travel for the month is {budgets[status_month]["Travel"]}\n",
        f"Personal for the month is: {Personal} and budget for Personal expenses for the month is {budgets[status_month]["Personal"]}\n",
        f"Miscellaneuos for the month is: {Miscellaneuos} and the budget for Miscellaneuos expenses for the month is {budgets[status_month]["Miscellaneuos"]}\n",
    )
    
     
def save_files():
    global all_transactions_list
    global save_all_transactions_list
    save_all_transactions_list = []
    i = 0
    for a in all_transactions_list:
        entries = list(a)
        save_all_transactions_list.append(entries)
        i += 1
    for b in save_all_transactions_list:
        b[0] = b[0].strftime("%d/%m/%Y")
    with open('all_transactions_list.json','w') as file:
        json.dump(save_all_transactions_list,file,indent=4)
    global budgets
    global save_budgets
    save_budgets = {}
    j = 0
    for key,value in budgets.items():
        key_save = key.strftime("%m/%Y")
        save_budgets[key_save] = value
    with open('budgets.json','w') as dict_file:
        json.dump(save_budgets,dict_file,indent=4)


def load_files():
    global all_transactions_list
    if os.path.exists('all_transactions_list.json'):
        with open('all_transactions_list.json', 'r') as list_file:
            save_all_transactions_list = json.load(list_file)
        num = 0
        for i in save_all_transactions_list:
            i[0] = datetime.strptime(i[0],"%d/%m/%Y")
            i = tuple(i)
            save_all_transactions_list[num] = i
            num += 1
        all_transactions_list = list(save_all_transactions_list)
    else:
        all_transactions_list = []
    global budgets
    if os.path.exists('budgets.json'):
        with open('budgets.json','r') as budgets_dict:
            save_budgets = json.load(budgets_dict)
        for key,value in save_budgets.items():
            chng_key = datetime.strptime(key, "%m/%Y")
            budgets[chng_key] = value
    else:
        budgets = {}


def reports():



def main():
    load_files()
    while True:
        main_menu()
        entry = user_menu_input()
        if entry == 1:
            add_transactions()
        elif entry == 2:
            view_transactions()
        elif entry == 3:
            view_transactions_category()
        elif entry == 4:
            summary()
        elif entry == 5:
            set_budget()
        elif entry == 6:
            budget_status()
        elif entry == 7:
            reports()
        elif entry == 8:
            save_files()
            break
        elif entry not in {1, 2, 3, 4, 5, 6, 7, 8} or entry == -1:
            print("Enter valid input!!!")




#starting the program
main()
