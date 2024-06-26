import mysql.connector
from mysql.connector import Error
from datetime import datetime
from prettytable import PrettyTable

# Connection to the MySQL database
try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="@Ryan007",
        database="mysql"
    )

    if connection.is_connected():
        cursor = connection.cursor()
        
        # Create the Students table if it does not already exist
        create_students_table = """
        CREATE TABLE IF NOT EXISTS Students (
            StudentID INT AUTO_INCREMENT PRIMARY KEY,
            FirstName VARCHAR(50) NOT NULL,
            LastName VARCHAR(50) NOT NULL,
            DateOfBirth DATE,
            Gender ENUM('Male', 'Female', 'Other'),
            Email VARCHAR(100) UNIQUE,
            PhoneNumber VARCHAR(15),
            EnrollmentDate DATE NOT NULL
        );
        """
        cursor.execute(create_students_table)
        connection.commit()

        # Retrieve the table data
        def show():
            query = "SELECT * FROM Students"
            cursor.execute(query)
            rows = cursor.fetchall()
            table = PrettyTable()
            table.field_names = ["StudentID", "FirstName", "LastName", "DateOfBirth", "Gender", "Email", "PhoneNumber", "EnrollmentDate"]
            
            for row in rows:
                table.add_row(row)
        
            print("Students Table:")
            print(table)

        # Insert data
        def insert_student(first_name, last_name, date_of_birth, gender, email, phone_number, enrollment_date):
            insert_query = """
                INSERT INTO Students (FirstName, LastName, DateOfBirth, Gender, Email, PhoneNumber, EnrollmentDate)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
            cursor.execute(insert_query, (first_name, last_name, date_of_birth, gender, email, phone_number, enrollment_date))
            connection.commit()

        # Delete data
        def delete_student(student_id):
            delete_query = "DELETE FROM Students WHERE StudentID = %s"
            cursor.execute(delete_query, (student_id,))
            connection.commit()

        # Update data
        def update_student(student_id, first_name=None, last_name=None, date_of_birth=None, gender=None, email=None, phone_number=None, enrollment_date=None):
            update_query = "UPDATE Students SET "
            update_fields = []
            update_values = []
                    
            if first_name:
                update_fields.append("FirstName = %s")
                update_values.append(first_name)
            if last_name:
                update_fields.append("LastName = %s")
                update_values.append(last_name)
            if date_of_birth:
                update_fields.append("DateOfBirth = %s")
                update_values.append(date_of_birth)
            if gender:
                update_fields.append("Gender = %s")
                update_values.append(gender)
            if email:
                update_fields.append("Email = %s")
                update_values.append(email)
            if phone_number:
                update_fields.append("PhoneNumber = %s")
                update_values.append(phone_number)
            if enrollment_date:
                update_fields.append("EnrollmentDate = %s")
                update_values.append(enrollment_date)
                    
            update_query += ", ".join(update_fields)
            update_query += " WHERE StudentID = %s"
            update_values.append(student_id)
                    
            cursor.execute(update_query, update_values)
            connection.commit()

        # Search students
        def search_students(column, value):
            query = f"SELECT * FROM Students WHERE {column} = %s"
            cursor.execute(query, (value,))
            results = cursor.fetchall()
            if results:
                print("Search Results:")
                for row in results:
                    print(row)
            else:
                print("No records found.")

        print("Welcome!!! To the student management system")

        while True:
            print("\nMain Menu")
            print("1.INSERT DATA\n2.DELETE DATA\n3.UPDATE DATA\n4.SEARCH DATA\n5.SHOW DATA\n6.EXIT")
            c = int(input("Enter your choice: "))

            if c == 1:
                first_name = input("Enter first name: ")
                last_name = input("Enter last name: ")
                date_of_birth = input("Enter date of birth (YYYY-MM-DD): ")
                gender = input("Enter gender (Male, Female, Other): ")
                email = input("Enter email: ")
                phone_number = input("Enter phone number: ")
                enrollment_date = input("Enter enrollment date (YYYY-MM-DD): ")

                insert_student(first_name, last_name, date_of_birth, gender, email, phone_number, enrollment_date)

            elif c == 2:
                student_id = input("Enter the StudentID of the student to delete: ")
                delete_student(student_id)
            
            elif c == 3:
                student_id = input("Enter the StudentID of the student you want to update: ")
                print("Enter the new values (leave blank to keep current value):")

                first_name = input("Enter new first name: ") or None
                last_name = input("Enter new last name: ") or None
                date_of_birth = input("Enter new date of birth (YYYY-MM-DD): ") or None
                gender = input("Enter new gender (Male, Female, Other): ") or None
                email = input("Enter new email: ") or None
                phone_number = input("Enter new phone number: ") or None
                enrollment_date = input("Enter new enrollment date (YYYY-MM-DD): ") or None

                update_student(student_id, first_name, last_name, date_of_birth, gender, email, phone_number, enrollment_date)

            elif c == 4:
                column = input("Enter the column name to search by (e.g., FirstName, LastName, Email): ")
                value = input(f"Enter the value to search for in {column}: ")

                search_students(column, value)
            
            elif c == 5:
                show()

            elif c == 6:
                print("Exiting the system.")
                break

            else:
                print("Invalid choice. Please try again.")

except Error as e:
    print(f"Error: {e}")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed.")