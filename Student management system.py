import json

FILE_NAME = "students.json"


# Asks the user for text and keeps asking until they type something (not empty).
def get_text(prompt):
    while True:
        value = input(prompt).strip()
        if value == "":
            print("  Input cannot be empty. Please try again.")
        else:
            return value


# Asks the user for a whole number (like age) and keeps asking until it is valid.
def get_int(prompt):
    while True:
        value = input(prompt).strip()
        try:
            number = int(value)
            if number <= 0:
                print("  Please enter a number greater than 0.")
            else:
                return number
        except ValueError:
            print("  Invalid input. Please enter a whole number.")


# Asks the user for marks (0 to 100, decimals allowed) and keeps asking until valid.
def get_marks(prompt):
    while True:
        value = input(prompt).strip()
        try:
            marks = float(value)
            if marks < 0 or marks > 100:
                print("  Marks must be between 0 and 100.")
            else:
                return marks
        except ValueError:
            print("  Invalid input. Please enter a number.")


# Looks through the list and returns the student with the given ID, or None if not found.
def find_by_id(students, student_id):
    for student in students:
        if student["id"] == student_id:
            return student
    return None


# Prints one student's details on a single formatted row.
def print_student_row(student):
    print(f"{student['id']:<8}{student['name']:<20}{student['age']:<6}"
          f"{student['course']:<18}{student['marks']:<6}")


# Prints the column headings for the student table.
def print_header():
    print(f"{'ID':<8}{'Name':<20}{'Age':<6}{'Course':<18}{'Marks':<6}")
    print("-" * 58)


# Adds a new student after validating the input and making sure the ID is unique.
def add_student(students):
    print("\n--- Add Student ---")
    student_id = get_text("Enter ID: ")
    if find_by_id(students, student_id) is not None:
        print("A student with this ID already exists. Record not added.")
        return

    name = get_text("Enter name: ")
    age = get_int("Enter age: ")
    course = get_text("Enter course: ")
    marks = get_marks("Enter marks (0-100): ")

    student = {"id": student_id, "name": name, "age": age,
               "course": course, "marks": marks}
    students.append(student)
    save_data(students)
    print("Student added successfully!")


# Shows every student in a neat table, or a message if there are none.
def view_students(students):
    print("\n--- All Students ---")
    if len(students) == 0:
        print("No student records found.")
        return

    print_header()
    for student in students:
        print_student_row(student)
    print(f"\nTotal students: {len(students)}")


# Searches for students by ID (exact match) or by name (partial, ignores case).
def search_student(students):
    print("\n--- Search Student ---")
    print("1. Search by ID")
    print("2. Search by Name")
    choice = input("Choose an option: ").strip()

    if choice == "1":
        student_id = get_text("Enter ID: ")
        results = []
        student = find_by_id(students, student_id)
        if student is not None:
            results.append(student)
    elif choice == "2":
        name = get_text("Enter name (or part of it): ").lower()
        results = []
        for student in students:
            if name in student["name"].lower():
                results.append(student)
    else:
        print("Invalid choice.")
        return

    if len(results) == 0:
        print("Student not found.")
    else:
        print()
        print_header()
        for student in results:
            print_student_row(student)


# Updates a student's details; pressing Enter on a field keeps the old value.
def update_student(students):
    print("\n--- Update Student ---")
    student_id = get_text("Enter ID of the student to update: ")
    student = find_by_id(students, student_id)

    if student is None:
        print("Student not found.")
        return

    print("Leave a field empty and press Enter to keep the current value.")

    new_name = input(f"Name [{student['name']}]: ").strip()
    if new_name != "":
        student["name"] = new_name

    new_age = input(f"Age [{student['age']}]: ").strip()
    if new_age != "":
        try:
            age = int(new_age)
            if age > 0:
                student["age"] = age
            else:
                print("  Age must be greater than 0. Keeping old age.")
        except ValueError:
            print("  Invalid age. Keeping old age.")

    new_course = input(f"Course [{student['course']}]: ").strip()
    if new_course != "":
        student["course"] = new_course

    new_marks = input(f"Marks [{student['marks']}]: ").strip()
    if new_marks != "":
        try:
            marks = float(new_marks)
            if 0 <= marks <= 100:
                student["marks"] = marks
            else:
                print("  Marks must be between 0 and 100. Keeping old marks.")
        except ValueError:
            print("  Invalid marks. Keeping old marks.")

    save_data(students)
    print("Student updated successfully!")


# Deletes a student by ID after asking the user to confirm.
def delete_student(students):
    print("\n--- Delete Student ---")
    student_id = get_text("Enter ID of the student to delete: ")
    student = find_by_id(students, student_id)

    if student is None:
        print("Student not found.")
        return

    confirm = input(f"Delete {student['name']}? (y/n): ").strip().lower()
    if confirm == "y":
        students.remove(student)
        save_data(students)
        print("Student deleted successfully!")
    else:
        print("Deletion cancelled.")


# Writes the whole student list to the JSON file.
def save_data(students):
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(students, file, indent=4)
    except OSError:
        print("Error: could not save data to file.")


# Reads the student list from the JSON file; returns an empty list if there is no file yet.
def load_data():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("No saved data found. Starting with an empty list.")
        return []
    except json.JSONDecodeError:
        print("Data file is damaged or empty. Starting with an empty list.")
        return []


# Shows the main menu on the screen.
def show_menu():
    print("\n==============================")
    print("   STUDENT MANAGEMENT SYSTEM")
    print("==============================")
    print("1. Add Student")
    print("2. View All Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Exit")


# Runs the program: loads data, then shows the menu in a loop until the user exits.
def main():
    students = load_data()

    while True:
        show_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_students(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            update_student(students)
        elif choice == "5":
            delete_student(students)
        elif choice == "6":
            save_data(students)
            print("Data saved. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


main()