# Expense and Budget app.

# I created this program so that a user can:
# - View, add, update and delete all and any expenses they make,
# - View, add, update and delete all and any income they gain,
# - View, update, delete and set a budget on any category,
# - View, update, delete, set financial goals and view their progress towards said financial goal
# depending on their total income and expenses.
# This data is then stored and updated on a database using SQL.


# Importing sqlite3.
import sqlite3

# Function to create the database and tables if they do not exist.
def create_database_and_tables():
    try:
        db = sqlite3.connect('expense_budget_app.db')
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS expense (
                        id INTEGER PRIMARY KEY,
                        category TEXT,
                        amount REAL,
                        date TEXT
                        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS income (
                        id INTEGER PRIMARY KEY,
                        category TEXT,
                        amount REAL,
                        date TEXT
                        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS budgets (
                        id INTEGER PRIMARY KEY,
                        category TEXT UNIQUE,
                        budget REAL
                        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS goals (
                        id INTEGER PRIMARY KEY,
                        goal TEXT UNIQUE,
                        amount REAL,
                        date TEXT
                        )''')
        
        db.commit()
    except sqlite3.Error as error:
        print('Error:', error)
    finally:
        db.close()


# Function to populate initial values if needed.
def populate_initial_values():
    try:
        db = sqlite3.connect('expense_budget_app.db')
        cursor = db.cursor()

        # Add initial values to tables if needed.

        db.commit()
    except sqlite3.Error as error:
        print('Error:', error)
    finally:
        db.close()


# Main function to display menu and execute user's choice.
def main():
    create_database_and_tables()
    populate_initial_values()

    while True:
        print('\nMenu:')
        print('\n1. Add expense.')
        print('2. View expenses or ID.')
        print('3. View expenses or ID by category.')
        print('4. Update expenses.')
        print('5. Delete expenses')
        print('\n6. Add income.')
        print('7. View income or ID.')
        print('8. View income or ID by category.')
        print('9. Update income.')
        print('10. Delete income')
        print('\n11. View total amount of expenses, income and goals. *')
        print('12. Set budget for a category.')
        print('13. View budget for all categories.')
        print('14. Update a budget')
        print('15. Delete a budget')
        print('\n16. Set financial goals.')
        print('17. View progress towards financial goals. *')
        print('18. Update financial goals.')
        print('19. Delete financial goals.')
        print('\n0. Exit')

        choice = input('\nPlease enter your choice: ')
        if choice.isdigit():
            choice = int(choice)
            if choice == 1:
                add_expense()
            elif choice == 2:
                view_expenses()
            elif choice == 3:
                view_expense_by_category()
            elif choice == 4:
                update_expenses()
            elif choice == 5:
                delete_expense()
            elif choice == 6:
                add_income()
            elif choice == 7:
                view_income()
            elif choice == 8:
                view_income_by_category()
            elif choice == 9:
                update_income()
            elif choice == 10:
                delete_income()
            elif choice == 11:
                total_amount()
            elif choice == 12:
                set_budget_for_a_category()
            elif choice == 13:
                view_budget_for_all_categories()
            elif choice == 14:
                update_budget()
            elif choice == 15:
                delete_budget()
            elif choice == 16:
                set_financial_goals()
            elif choice == 17:
                view_financial_goals_with_net_total()
            elif choice == 18:
                update_financial_goals()
            elif choice == 19:
                delete_financial_goal()
            elif choice == 0:
                print('\nThank you for using the expense and budget tracker app. Have a great day!\n')
                break
            else:
                print(f"\nInvalid choice '{choice}'. Please enter a valid number.")
                print('(Options 1 - 19 or 0 to exit.)')
        else:
            print(f"\nInvalid input '{choice}'. Please enter a valid number.")
            print('(Options 1 - 19 or 0 to exit.)')


# 1 Function to add a new expense to the database.
def add_expense():
    try:
        category = input('\nEnter expense category: ').lower()
        while True:
            try:
                amount_input = input('Enter expense amount: ')
                amount_float = float(amount_input)
                break
            except ValueError:
                print('\nInvalid input. Please enter a valid number.')
        date = input('Enter expense date (YYYY-MM-DD): ')

        db = sqlite3.connect('expense_budget_app.db')
        cursor = db.cursor()
        cursor.execute('''INSERT INTO expense (category, amount, date)
                        VALUES (?, ?, ?)''', (category, amount_float, date))
        db.commit()
        print(f"\nExpense added successfully '{category} - {amount_float}'!")
    except sqlite3.Error as error:
        print('Error:', error)
    finally:
        db.close()


# 2 Function to view expenses in the database.
def view_expenses():
    try:
        db = sqlite3.connect('expense_budget_app.db')
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM expense''')
        expenses = cursor.fetchall()
        if not expenses:
            print('\nNo expenses found.')
        else:
            print('\nExpense ID  |      Category          | Amount       | Date') 
            print('----------------------------------------------------------------')
            for expense in expenses:
                print('{:<11} | {:<22} | {:<12} | {}'.format(expense[0], expense[1], expense[2], expense[3]))
    except sqlite3.Error as error:
        print('Error:', error)
    finally:
        db.close()


# 3 Function to view expense by category in the database.
def view_expense_by_category():
    try:
        db = sqlite3.connect('expense_budget_app.db')
        cursor = db.cursor()
        category = input('\nEnter the category to view expenses for: ').lower() 
        cursor.execute('''SELECT * FROM expense WHERE LOWER(category) = ?''', (category,))
        expenses = cursor.fetchall()
        if not expenses:
            print(f'\nNo expenses found for the category: ({category.capitalize()})')
        else:
            print('\nExpense ID  |      Category          | Amount       | Date')
            print('----------------------------------------------------------------')
            for expense in expenses:
                print('{:<11} | {:<22} | {:<12} | {}'.format(expense[0], expense[1], expense[2], expense[3]))
    except sqlite3.Error as error:
        print('Error:', error)
    finally:
        db.close()


# 4 Function to update expenses, category, or date in the database.
def update_expenses():
    try:
        db = sqlite3.connect('expense_budget_app.db')
        cursor = db.cursor()
        expense_id = input('\nEnter the expense ID to update: ')
        cursor.execute('''SELECT * FROM expense WHERE id = ?''', (expense_id,))
        expense = cursor.fetchone()
        if not expense:
            print("\nExpense with ID '{}' not found.".format(expense_id))
            return
        
        print('\nExpense Details:')
        print('Expense ID: ', expense[0])
        print('Category: ', expense[1])
        print('Amount: ', expense[2])
        print('Date: ', expense[3])
        
        print('\nSelect field to update:')
        print('Options 1, 2, 3 or 4.')
        print('\n1. Category')
        print('2. Amount')
        print('3. Date')
        print('4. Cancel changes')
        
        option = input('\nEnter your choice: ')
        if option == '1':
            field = 'category'
            new_value = input('Enter the new category: ')
        elif option == '2':
            field = 'amount'
            while True:
                new_value = input('Enter the new amount: ')
                try:
                    new_value = float(new_value)  # Converting to float for amount.
                    break 
                except ValueError:
                    print('\nInvalid input. Please enter a valid number.')
        elif option == '3':
            field = 'date'
            new_value = input('Enter the new date (YYYY-MM-DD): ')
        elif option == '4':
            print('\nChanges cancelled. Returning to menu.')
            return            
        else:
            print(f'\nInvalid option ({option}). Please enter either 1, 2, 3 or 4.')
            return
        
        cursor.execute('''UPDATE expense SET {} = ? WHERE id = ?'''.format(field), (new_value, expense_id))
        db.commit()
        print(f"\nExpense updated successfully '{field} - {new_value}'!")
        
    except sqlite3.Error as error:
        print('Error:', error)
    finally:
        db.close()


# 5 Function to delete expense.
def delete_expense():
    try:
        expense_id = int(input('\nPlease enter expense ID you wish to delete: '))
    except ValueError:
        print('\nInvalid input. Please enter a valid expense ID (a number ID).')
        print('(You can search for an expense number ID at the \'view expense\' option).')
        return
    db = sqlite3.connect('expense_budget_app.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM expense WHERE id=?', (expense_id,))
    expense = cursor.fetchone()
    if expense is None:
        print(f'\nExpense with ID ({expense_id}) has not been found.')
        print('(You can search for available expense number ID at the \'view expense\' option).')
    else:
        print('\nExpense Details:')
        print('Expense ID: ', expense[0])
        print('Category: ', expense[1])
        print('Amount: ', expense[2])
        print('Date: ', expense[3])
        # Ask if the user is sure they want to delete
        while True:
            confirmation = input(f'\nAre you sure you wish to delete Expense ID {expense_id}?\n\n1. Continue with the deletion.\n2. Disregard and go back to the main menu.\n\nEnter your choice: ')
            if confirmation == '1':
                # To have the expense saved to show the user once expense deleted.
                category = expense[1]
                cursor.execute('DELETE FROM expense WHERE id=?', (expense_id,))
                db.commit()
                print(f'\nExpense (ID: {expense_id}) - \'{category}\' has been deleted successfully.')
                break
            elif confirmation == '2':
                print('\nDeletion canceled. Returning to the main menu.')
                break
            else:
                print("\nInvalid choice. Please enter either '1' or '2'.")
    db.close()


# 6 Function to add income in the database.
def add_income():
    try:
        category = input('\nEnter income category: ').lower()
        while True:
            try:
                amount_input = input('Enter income amount: ')
                amount_float = float(amount_input)
                break
            except ValueError:
                print('\nInvalid input. Please enter a valid number.')
        date = input('Enter income date (YYYY-MM-DD): ')
        db = sqlite3.connect('expense_budget_app.db')
        cursor = db.cursor()
        cursor.execute('''INSERT INTO income (category, amount, date)
                        VALUES (?, ?, ?)''', (category, amount_float, date))
        db.commit()
        print(f"\nIncome added successfully '{category} - {amount_float}'!")
    except sqlite3.Error as error:
        print('Error:', error)
    finally:
        db.close()


# 7 Function to view income in the database.
def view_income():
    try:
        db = sqlite3.connect('expense_budget_app.db')
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM income''')
        income = cursor.fetchall()
        if not income:
            print('\nNo income found.')
        else:
            print('\nIncome ID   |      Category          | Amount       | Date')
            print('----------------------------------------------------------------')
            for incomes in income:
                print('{:<11} | {:<22} | {:<12} | {}'.format(incomes[0], incomes[1], incomes[2], incomes[3]))
    except sqlite3.Error as error:
        print('Error:', error)
    finally:
        db.close()


# 8 Function to view income by category in the database.
def view_income_by_category():
    try:
        db = sqlite3.connect('expense_budget_app.db')
        cursor = db.cursor()
        category = input('\nEnter the category to view income for: ').lower()
        cursor.execute('''SELECT * FROM income WHERE LOWER(category) = ?''', (category,))
        income = cursor.fetchall()
        if not income:
            print(f'\nNo income found for the category: ({category.capitalize()})')
        else:
            print('\nIncome ID   |      Category          | Amount       | Date')
            print('----------------------------------------------------------------')
            for incomes in income:
                print('{:<11} | {:<22} | {:<12} | {}'.format(incomes[0], incomes[1], incomes[2], incomes[3]))
    except sqlite3.Error as error:
        print('Error:', error)
    finally:
        db.close()


# 9 Function to update income, category, or date in the database.
def update_income():
    try:
        db = sqlite3.connect('expense_budget_app.db')
        cursor = db.cursor()
        income_id = input('\nEnter the income ID to update: ')
        cursor.execute('''SELECT * FROM income WHERE id = ?''', (income_id,))
        income = cursor.fetchone()
        if not income:
            print("\nIncome with ID '{}' not found.".format(income_id))
            return
        
        print('\nIncome Details:')
        print('Income ID: ', income[0])
        print('Category: ', income[1])
        print('Amount: ', income[2])
        print('Date: ', income[3])
        print('\nSelect field to update:')
        print('Options 1, 2, 3 or 4.')
        print('\n1. Category')
        print('2. Amount')
        print('3. Date')
        print('4. Cancel changes')
        
        option = input('\nEnter your choice: ')
        if option == '1':
            field = 'category'
            new_value = input('Enter the new category: ')
        elif option == '2':
            field = 'amount'
            while True:
                new_value = input('Enter the new amount: ')
                try:
                    new_value = float(new_value)
                    break 
                except ValueError:
                    print('\nInvalid input. Please enter a valid number.')
        elif option == '3':
            field = 'date'
            new_value = input('Enter the new date (YYYY-MM-DD): ')
        elif option == '4':
            print('\nChanges cancelled. Returning to menu.')
            return            
        else:
            print(f'\nInvalid option ({option}). Please enter either 1, 2, 3 or 4.')
            return
        
        cursor.execute('''UPDATE income SET {} = ? WHERE id = ?'''.format(field), (new_value, income_id))
        db.commit()
        print(f"\nIncome updated successfully '{field} - {new_value}'!")
        
    except sqlite3.Error as error:
        print('Error:', error)
    finally:
        db.close()


# 10 Function to delete income.
def delete_income():
    try:
        income_id = int(input('\nPlease enter income ID you wish to delete: '))
    except ValueError:
        print('\nInvalid input. Please enter a valid income ID (a number ID).')
        print('(You can search for an income number ID at the \'view income\' option).')
        return
    db = sqlite3.connect('expense_budget_app.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM income WHERE id=?', (income_id,))
    income = cursor.fetchone()
    if income is None:
        print(f'\nIncome with ID ({income_id}) has not been found.')
        print('(You can search for available income number ID at the \'view income\' option).')
    else:
        print('\nIncome Details:')
        print('Income ID: ', income[0])
        print('Category: ', income[1])
        print('Amount: ', income[2])
        print('Date: ', income[3])
        # Ask if the user is sure they want to delete.
        while True:
            confirmation = input(f"\nAre you sure you wish to delete Income ID '{income_id}'?\n\n1. Continue with the deletion.\n2. Disregard and go back to the main menu.\n\nEnter your choice: ")
            if confirmation == '1':
                # To have the income saved to show the user once income deleted.
                category = income[1]
                cursor.execute('DELETE FROM income WHERE id=?', (income_id,))
                db.commit()
                print(f'\nIncome (ID: {income_id}) - \'{category}\' has been deleted successfully.')
                break
            elif confirmation == '2':
                print('\nDeletion canceled. Returning to the main menu.')
                break
            else:
                print("\nInvalid choice. Please enter either '1' or '2'.")
    db.close()


# 11 Function to view total amount of expenses, income, and total needed for financial goals.
def total_amount():
    try:
        db = sqlite3.connect('expense_budget_app.db')
        cursor = db.cursor()
        cursor.execute('''SELECT SUM(amount) FROM expense''')
        total_expense = cursor.fetchone()[0]
        if total_expense is None:
            total_expense = 0

        cursor.execute('''SELECT SUM(amount) FROM income''')
        total_income = cursor.fetchone()[0]
        if total_income is None:
            total_income = 0

        cursor.execute('''SELECT SUM(amount) FROM goals''')
        total_goals = cursor.fetchone()[0]
        if total_goals is None:
            total_goals = 0

        net_total = total_income - total_expense
        total_needed_for_goals = total_goals - net_total

        print('\n-------------------------------------')
        print('Total Expenses: {:.2f}'.format(total_expense))
        print('Total Income: {:.2f}'.format(total_income))
        print('Net Total: {:.2f}'.format(net_total))
        print('Total Needed for Goals: {:.2f}'.format(total_needed_for_goals))
        print('-------------------------------------')

    except sqlite3.Error as error:
        print('Error:', error)


# 12 Function to set budget for a category.
def set_budget_for_a_category():
    try:
        db = sqlite3.connect('expense_budget_app.db')
        cursor = db.cursor()
        category = input('\nEnter the category to set budget for: ').lower()
        while True:
            try:
                budget = float(input('Enter the budget for this category: '))
                if budget < 0:
                    print('Budget cannot be negative. Please enter a valid amount.')
                else:
                    break
            except ValueError:
                print('\nInvalid input. Please enter a valid number.')

        cursor.execute('''INSERT OR REPLACE INTO budgets (category, budget)
                        VALUES (?, ?)''', (category, budget))
        db.commit()
        print(f"\nBudget set successfully for '{category.capitalize()} - {budget}'!")

    except sqlite3.Error as error:
        print('Error:', error)
    finally:
        db.close()


# 13 Function to view budget for all categories along with total expenses for each category.
def view_budget_for_all_categories():
    try:
        db = sqlite3.connect('expense_budget_app.db')
        cursor = db.cursor()
        cursor.execute('''SELECT b.category, b.budget, COALESCE(SUM(e.amount), 0) AS total_expense
                        FROM budgets AS b
                        LEFT JOIN expense AS e ON b.category = e.category
                        GROUP BY b.category''')
        budgets = cursor.fetchall()
        if not budgets:
            print('\nNo budgets set.')
        else:
            print('\nCategory           | Budget       | Total Expense')
            print('---------------------------------------------------')
            for budget in budgets:
                category = budget[0]
                budget_amount = budget[1]
                total_expense = budget[2]
                print('{:<18} | {:<12.2f} | {:.2f}'.format(category, budget_amount, total_expense))
    except sqlite3.Error as error:
        print('Error:', error)
    finally:
        db.close()


# 14 Function to update a budget.
def update_budget():
    try:
        db = sqlite3.connect('expense_budget_app.db')
        cursor = db.cursor()
        category = input('\nEnter the category for which you want to update the budget: ').lower()
        cursor.execute('''SELECT * FROM budgets WHERE LOWER(category) = ?''', (category,))
        existing_budget = cursor.fetchone()
        if not existing_budget:
            print(f'\nNo budget found for category "{category.capitalize()}".')
            return
        else:
            print(f'\nExisting Budget for Category "{category.capitalize()}": {existing_budget[1]}')
            while True:
                try:
                    new_budget = float(input('Enter the new budget: '))
                    if new_budget < 0:
                        print('Budget cannot be negative. Please enter a valid amount.')
                    else:
                        break
                except ValueError:
                    print('\nInvalid input. Please enter a valid number.')
            
            cursor.execute('''UPDATE budgets SET budget = ? WHERE LOWER(category) = ?''', (new_budget, category))
            db.commit()
            print(f"\nBudget for category '{category.capitalize()} - {new_budget}' updated successfully!")
    except sqlite3.Error as error:
        print('Error:', error)
    finally:
        db.close()


# 15 Function to delete a budget.
def delete_budget():
    try:
        db = sqlite3.connect('expense_budget_app.db')
        cursor = db.cursor()
        category = input('\nEnter the category for which you want to delete the budget: ').lower()
        cursor.execute('''SELECT * FROM budgets WHERE LOWER(category) = ?''', (category,))
        existing_budget = cursor.fetchone()
        if not existing_budget:
            print(f'\nNo budget found for category "{category.capitalize()}".')
            return
        else:
            confirmation = input(f'\nAre you sure you wish to delete the budget for category "{category.capitalize()}"?\n\n1. Continue with the deletion.\n2. Disregard and go back to the main menu.\n\nEnter your choice: ')
            if confirmation == '1':
                cursor.execute('''DELETE FROM budgets WHERE LOWER(category) = ?''', (category,))
                db.commit()
                print(f'\nBudget for category "{category.capitalize()}" deleted successfully!')
            elif confirmation == '2':
                print('\nDeletion canceled. Returning to the main menu.')
            else:
                print("\nInvalid choice. Please enter either '1' or '2'.")
    except sqlite3.Error as error:
        print('Error:', error)
    finally:
        db.close()


# 16 Function to set financial goals.
def set_financial_goals():
    try:
        db = sqlite3.connect('expense_budget_app.db')
        cursor = db.cursor()
        goal_title = input('\nEnter a title for your financial goal: ').lower()
        while True:
            try:
                goal_amount = float(input('Enter the amount you need for this financial goal: '))
                if goal_amount < 0:
                    print('Goal cannot be negative. Please enter a valid amount.')
                else:
                    break
            except ValueError:
                print('\nInvalid input. Please enter a valid number.')
        goal_date = input('Enter the date by which you want to achieve this goal (YYYY-MM-DD): ')
        cursor.execute('''INSERT OR REPLACE INTO goals (goal, amount, date)
                        VALUES (?, ?, ?)''', (goal_title, goal_amount, goal_date))
        db.commit()
        print(f"\nFinancial goal set successfully for '{goal_title.capitalize()} - {goal_amount}'!")
    except sqlite3.Error as error:
        print('Error:', error)
    finally:
        db.close()


# 17 Function to view financial goals along with net total, amount needed to reach goal, and goal date.
def view_financial_goals_with_net_total():
    try:
        db = sqlite3.connect('expense_budget_app.db')
        cursor = db.cursor()

        cursor.execute('''SELECT * FROM goals''')
        goals = cursor.fetchall()

        total_income = 0
        cursor.execute('''SELECT SUM(amount) FROM income''')
        total_income_result = cursor.fetchone()
        if total_income_result:
            total_income = total_income_result[0] or 0

        total_expense = 0
        cursor.execute('''SELECT SUM(amount) FROM expense''')
        total_expense_result = cursor.fetchone()
        if total_expense_result:
            total_expense = total_expense_result[0] or 0

        net_total = total_income - total_expense

        # Display financial goals along with net total, difference, and goal date.
        if not goals:
            print('\nNo financial goals set.')
        else:
            print('\nFinancial Goals and amount needed to reach Goals:')
            print('----------------------------------------------------------------------------------------------------------------|')
            print('| Goal ID  |            Goal                |    Amount    |       Goal Date      |   Net Total  | Amount Needed|')
            print('|----------|--------------------------------|--------------|----------------------|--------------|--------------|')
            for goal in goals:
                goal_id = goal[0]
                goal_name = goal[1]
                goal_amount = goal[2]
                goal_date = goal[3] if goal[3] else "Not set"  # If goal date is not set.
                difference = goal_amount - net_total
                print('| {:<8} | {:<30} | {:>12.2f} | {:>20} | {:>12.2f} | {:>12.2f} |'.format(goal_id, goal_name, goal_amount, goal_date, net_total, difference))
            print('|---------------------------------------------------------------------------------------------------------------|')

    except sqlite3.Error as error:
        print('Error:', error)
    finally:
        db.close()


# 18 Function to update financial goals.
def update_financial_goals():
    try:
        db = sqlite3.connect('expense_budget_app.db')
        cursor = db.cursor()
        
        goal_id = input('\nEnter the ID of the financial goal you want to edit: ')
        cursor.execute('''SELECT * FROM goals WHERE id = ?''', (goal_id,))
        goal = cursor.fetchone()
        if not goal:
            print(f'\nFinancial goal with ID ({goal_id}) not found.')
            return

        print('\nCurrent Financial Goal Details:')
        print('Goal ID:', goal[0])
        print('Goal:', goal[1])
        print('Amount:', goal[2])
        print('Date:', goal[3])

        new_goal_title = input('\nEnter a new title for the financial goal (or press Enter to keep the current title): ').lower()
        new_goal_amount = input('Enter a new amount for the financial goal (or press Enter to keep the current amount): ')
        new_goal_date = input('Enter a new date for the financial goal (YYYY-MM-DD) (or press Enter to keep the current date): ')

        if new_goal_title:
            cursor.execute('''UPDATE goals SET goal = ? WHERE id = ?''', (new_goal_title, goal_id))
        if new_goal_amount:
            try:
                new_goal_amount = float(new_goal_amount)
                cursor.execute('''UPDATE goals SET amount = ? WHERE id = ?''', (new_goal_amount, goal_id))
            except ValueError:
                print('Invalid input for amount. Please enter a valid number.')
        if new_goal_date:
            cursor.execute('''UPDATE goals SET date = ? WHERE id = ?''', (new_goal_date, goal_id))

        db.commit()
        print(f"\nFinancial goal updated successfully '{goal_id} - {new_goal_title} - {new_goal_amount} - {new_goal_date}'!")

    except sqlite3.Error as error:
        print('Error:', error)
    finally:
        db.close()


# 19 Function to delete a financial goal.
def delete_financial_goal():
    try:
        db = sqlite3.connect('expense_budget_app.db')
        cursor = db.cursor()
        goal_id = int(input('\nEnter the goal ID you want to delete: '))
        
        cursor.execute('''SELECT * FROM goals WHERE id = ?''', (goal_id,))
        goal = cursor.fetchone()
        if goal is None:
            print(f'\nFinancial goal with ID ({goal_id}) not found.')
            return
        else:
            goal_name = goal[1]
            goal_amount = goal[2]

            confirmation = input(f"\nAre you sure you wish to delete the financial goal with ID '{goal_id}' ({goal_name})?\n\n1. Continue with the deletion.\n2. Disregard and go back to the main menu.\n\nEnter your choice: ")
            if confirmation == '1':
                cursor.execute('DELETE FROM goals WHERE id=?', (goal_id,))
                db.commit()
                print(f'\nFinancial goal (ID: {goal_id}) - "{goal_name}" with amount {goal_amount} has been deleted successfully.')
            elif confirmation == '2':
                print('\nDeletion canceled. Returning to the main menu.')
            else:
                print("\nInvalid choice. Please enter either '1' or '2'.")
    except ValueError:
        print('\nInvalid input. Please enter a valid goal ID (a number ID).')
    except sqlite3.Error as error:
        print('Error:', error)
    finally:
        db.close()


