import datetime
# from datetime import datetime
import os

# validate date format
def validate_date_format(date_string):
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# validate yes/no response
def validate_yes_no(response):
    if response.lower() in ['yes', 'no']:
        return True
    else:
        return False

# register a user
def register_user():
    username = input("Enter a username: ")
    password = input("Enter a password: ")

    with open("users.txt", "a+") as f:
        f.seek(0)
        for line in f:
            user, _, _ = line.strip().split(",")
            if user == username:
                print("Username already exists!")
                return False

        f.write(f"{username},{password}\n")
        print("Registration successful!")
        return True

# validate user credentials
def validate_credentials(username, password):
    with open("user.txt", "r") as f:
        for line in f:
            if f"{username}, {password}" in line:
                return True
        return False

def count_users():
    with open("users.txt", "r") as f:
        count = len(f.readlines()) - 1
    return count

# add a task
def add_task():
    username = input("Enter the username of the person the task is assigned to: ")
    task_title = input("Enter the title of the task: ")
    task_description = input("Enter a description of the task: ")
    while True:
        due_date = input("Enter the due date of the task (yyyy-mm-dd): ")
        if validate_date_format(due_date):
            break
        else:
            print("Invalid date format. Please try again.")
    is_completed = input("Has the task been completed? (Yes/No): ")
    while not validate_yes_no(is_completed):
        is_completed = input("Invalid response. Has the task been completed? (Yes/No): ")
    with open("tasks.txt", "a") as f:
        f.write(f"{username}, {task_title}, {task_description}, {due_date}, {is_completed}\n")
    print("Task added successfully.")

# view all tasks
def view_all():
    with open("tasks.txt", "r") as f:
        task_details = [line.strip().split(", ") for line in f.readlines()]
    print("{:<15} {:<20} {:<30} {:<20} {:<15}".format("Assigned to", "Task", "Description", "Due Date", "Completed"))
    print("=" * 100)
    for task in task_details:
        print("{:<15} {:<20} {:<30} {:<20} {:<15}".format(task[0], task[1], task[2], task[3], task[4]))

# view tasks assigned to a specific user
def view_mine(username):
    with open("tasks.txt", "r") as f:
        task_details = [line.strip().split(", ") for line in f.readlines() if username == line.strip().split(", ")[0]]
    print("{:<20} {:<30} {:<20} {:<15}".format("Task", "Description", "Due Date", "Completed"))
    print("=" * 75)
    for task in task_details:
        print("{:<20} {:<30} {:<20} {:<15}".format(task[1], task[2], task[3], task[4]))

def generate_task_overview():
    """
        This function generates a report of all the tasks on the system
        """
    tasks = open("tasks.txt", "r")
    task_details = tasks.readlines()
    tasks.close()
    total_tasks = len(task_details)
    completed_tasks = 0
    uncompleted_tasks = 0
    overdue_tasks = 0

    for task in task_details:
        task_info = task.strip().split(", ")
        task_status = task_info[3]
        if task_status == "Yes":
            completed_tasks += 1
        else:
            uncompleted_tasks += 1
            deadline = datetime.strptime(task_info[3], "%Y-%m-%d")
            today = datetime.today()
            if deadline < today:
                overdue_tasks += 1

    percent_incomplete = (uncompleted_tasks / total_tasks) * 100 if total_tasks != 0 else 0
    percent_overdue = (overdue_tasks / total_tasks) * 100 if total_tasks != 0 else 0

    task_overview = open("task_overview.txt", "w")
    task_overview.write("Task Overview\n")
    task_overview.write(f"Total tasks: {total_tasks}\n")
    task_overview.write(f"Completed tasks: {completed_tasks}\n")
    task_overview.write(f"Uncompleted tasks: {uncompleted_tasks}\n")
    task_overview.write(f"Overdue tasks: {overdue_tasks}\n")
    task_overview.write(f"Percentage incomplete: {percent_incomplete:.2f}%\n")
    task_overview.write(f"Percentage overdue: {percent_overdue:.2f}%\n")
    task_overview.close()


def generate_user_overview():
    """
    This function generates a report of all the users on the system
    """
    users_file = open("users.txt", "r")
    users = users_file.readlines()
    tasks_file = open("tasks.txt", "r")
    tasks = tasks_file.readlines()

    num_users = count_users()
    task_count = len(tasks)
    assigned_tasks = {}
    task_statuses = {"completed": 0, "not_completed": 0, "overdue": 0}

    # Loop through all tasks to get assignment details
    for task in tasks:
        task_info = task.strip().split(", ")
        assigned_user = task_info[0]
        status = task_info[-1]
        if assigned_user not in assigned_tasks:
            assigned_tasks[assigned_user] = {"total_tasks": 0, "completed_tasks": 0, "not_completed_tasks": 0, "overdue_tasks": 0}
        assigned_tasks[assigned_user]["total_tasks"] += 1
        if status == "Yes":
            assigned_tasks[assigned_user]["completed_tasks"] += 1
            task_statuses["completed"] += 1
        else:
            assigned_tasks[assigned_user]["not_completed_tasks"] += 1
            task_due_date = datetime.strptime(task_info[3], "%Y-%m-%d")
            if task_due_date < datetime.today():
                assigned_tasks[assigned_user]["overdue_tasks"] += 1
                task_statuses["overdue"] += 1
            else:
                task_statuses["not_completed"] += 1

    # Write report to file
    user_overview = open("user_overview.txt", "w")
    user_overview.write("User Overview\n")
    user_overview.write(f"Total users: {num_users}\n")
    user_overview.write(f"Total tasks: {task_count}\n")
    user_overview.write(f"Completed tasks: {task_statuses['completed']}\n")
    user_overview.write(f"Tasks not completed: {task_statuses['not_completed']}\n")
    user_overview.write(f"Tasks overdue: {task_statuses['overdue']}\n")
    user_overview.write("\nUser task overview\n")
    for user in users:
        user_info = user.strip().split(", ")
        user_name = user_info[0]
        user_tasks = assigned_tasks.get(user_name, {"total_tasks": 0, "completed_tasks": 0, "not_completed_tasks": 0, "overdue_tasks": 0})
        user_task_percentage = round(user_tasks["total_tasks"] / task_count * 100, 2) if task_count > 0 else 0
        user_completed_percentage = round(user_tasks["completed_tasks"] / user_tasks["total_tasks"] * 100, 2) if user_tasks["total_tasks"] > 0 else 0
        user_not_completed_percentage = round(user_tasks["not_completed_tasks"] / user_tasks["total_tasks"] * 100, 2) if user_tasks["total_tasks"] > 0 else 0
        user_overdue_percentage = round(user_tasks["overdue_tasks"] / user_tasks["total_tasks"] * 100, 2) if user_tasks["total_tasks"] > 0 else 0
        user_overview.write(f"\nUser: {user_name}\n")
        user_overview.write(f"Total tasks assigned: {user_tasks['total_tasks']}\n")
        user_overview.write(f"Percentage of total tasks assigned: {user_task_percentage}%\n")
        user_overview.write(f"Percentage of tasks completed: {user_completed_percentage}%\n")
        user_overview.write(f"Percentage of tasks not completed: {user_not_completed_percentage}%\n")
        user_overview.write(f"Percentage of tasks overdue: {user_overdue_percentage}%\n")

    user_overview.close()

def main():
    """The main function that runs the program"""
    print("Welcome to the Task Manager Program!")
    print("Please login or register to continue.")
    username = input("Username: ")
    password = input("Password: ")
    if check_user_credentials(username, password):
        print(f"Welcome, {username}!")
        user_type = get_user_type(username)
        if user_type == "admin":
            admin_menu()
        else:
            user_menu(username)
    else:
        print("Invalid username or password.")


def check_user_credentials(username, password):
    """Checks if the provided username and password match a user in the users.txt file"""
    with open("users.txt", "r") as file:
        if file.readable():
            file.seek(0)
            for line in file:
                try:
                    user, pwd, role = line.strip().split(",")
                    if user == username and pwd == password:
                        return True
                except ValueError:
                    # line does not have expected format
                    continue
    return False


def get_user_type(username):
    """Returns the type of user (admin or user) based on their username"""
    with open("users.txt", "r") as file:
        if file.readable():
            file.seek(0)
            for line in file:
                try:
                    user, _, role = line.strip().split(",")
                    if user == username:
                        return role
                except ValueError:
                    # line does not have expected format
                    continue
    return None


def admin_menu():
    """The menu for the administrator"""
    while True:
        print("\nPlease select an option:")
        print("1 - Register User")
        print("2 - Add Task")
        print("3 - View All Users")
        print("4 - View All Tasks")
        print("5 - Generate Reports")
        print("0 - Logout")

        choice = input("Option: ")

        if choice == "1":
            register_user()
        elif choice == "2":
            add_task()
        elif choice == "3":
            view_all_users()
        elif choice == "4":
            view_all_tasks()
        elif choice == "5":
            generate_reports()
        elif choice == "0":
            print("Logging out...")
            break
        else:
            print("Invalid option. Please try again.")


def user_menu(username):
    """The menu for a regular user"""
    while True:
        print("\nPlease select an option:")
        print("1 - Add Task")
        print("2 - View My Tasks")
        print("3 - Logout")

        choice = input("Option: ")

        if choice == "1":
            add_task()
        elif choice == "2":
            view_mine(username)
        elif choice == "3":
            print("Logging out...")
            break
        else:
            print("Invalid option. Please try again.")


def register_user():
    """Registers a new user in the users.txt file"""
    username = input("Enter new username: ")
    password = input("Enter new password: ")
    confirm_password = input("Confirm new password: ")
    role = input("Enter user role (admin or user): ")

    if password != confirm_password:
        print("Passwords do not match. Please try again.")
        return

    with open("users.txt", "a+") as file:
        file.seek(0)
        if file.read(1) == '':
            # file is empty
            file.write(f"{username},{password},{role}")
            print("User registered successfully.")
        else:
            file.seek(0)
            for line in file:
                try:
                    user, _, _ = line.strip().split(",")
                    if user == username:
                        print("Username already exists. Please try again.")
                        break
                except ValueError:
                    # line does not have expected format
                    continue
            else:
                file.write(f"\n{username},{password},{role}")
                print("User registered successfully.")


def view_all_users():
    """Displays all users in the users.txt file"""
    print("All Users:")
    print("-----------")
    with open("users.txt", "r") as file:
        for line in file:
            try:
                user, _, role = line.strip().split(",")
                print(f"{user} ({role})")
            except ValueError:
                # Skip lines that don't have three values
                continue

def view_all_tasks():
    """
    This function displays all tasks to the user in a user-friendly manner
    """
    try:
        with open("tasks.txt", "r") as tasks_file:
            tasks = tasks_file.readlines()
            if tasks:
                print("{:<15} {:<20} {:<20} {:<25} {:<15} {}".format(
                    "Task number", "Task name", "Assigned to", "Task description", "Due date", "Completion"))
                for index, task in enumerate(tasks, start=1):
                    task_details = task.strip().split(",")
                    task_name = task_details[0]
                    assigned_to = task_details[1]
                    task_description = task_details[2]
                    due_date = task_details[3]
                    task_completion = task_details[4]
                    print("{:<15} {:<20} {:<20} {:<25} {:<15} {}".format(
                        index, task_name, assigned_to, task_description, due_date, task_completion))
            else:
                print("No tasks available.")
    except FileNotFoundError:
        print("File not found. Please contact the system administrator.")


def view_mine(username):
    """
    This function displays all tasks assigned to the logged in user in a user-friendly manner
    """
    try:
        with open("tasks.txt", "r") as tasks_file:
            tasks = tasks_file.readlines()
            if tasks:
                print("{:<15} {:<15} {:<25} {:<25} {:<15} {}".format(
                    "Task number", "Task name", "Assigned to", "Task description", "Due date", "Completion"))
                for index, task in enumerate(tasks, start=1):
                    task_details = task.strip().split(",")
                    task_name = task_details[0]
                    assigned_to = task_details[1]
                    if assigned_to == username:
                        task_description = task_details[2]
                        due_date = task_details[3]
                        task_completion = task_details[4]
                        print("{:<15} {:<15} {:<25} {:<25} {:<15} {}".format(
                            index, task_name, assigned_to, task_description, due_date, task_completion))
                else:
                    print("No tasks available for this user.")
            else:
                print("No tasks available.")
    except FileNotFoundError:
        print("File not found. Please contact the system administrator.")

def generate_reports():
    """
    Generates two reports: task_overview.txt which gives an overview of all the tasks, and
    user_overview.txt which gives an overview of all the users. Both files are saved in the same
    directory as the program.
    """
    generate_task_overview()
    generate_user_overview()

    # Open and read task overview file
    with open("task_overview.txt", "r") as task_file:
        task_data = task_file.read()

    # Open and read user overview file
    with open("user_overview.txt", "r") as user_file:
        user_data = user_file.read()

    # Print the contents of both files
    print(task_data)
    print(user_data)


main()

# I have added my files, tasks.txt you can keep blank, and in the users.txt file is the admin login details.