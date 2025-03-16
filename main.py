import sqlite3

class MySQL:
    def __init__(self):
        self.ConnectDB()
        self.CreateTB()

    def ConnectDB(self):
        self.connector = sqlite3.connect("students.db")
        self.c = self.connector.cursor()
    
    def CreateTB(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS students(
                       Id INTEGER PRIMARY KEY AUTOINCREMENT,
                       Name TEXT NOT NULL,
                       Age INTEGER,
                       Grade VARCHAR(40))""")
        self.connector.commit()

    def InsertDT(self):
        valid_grades = ["a", "b", "c"]
        num_students = int(input("How many students to add: "))
        for _ in range(num_students):
            name = input("Enter your name: ")
            
            while True:
                age = input("Enter your age: ")
                try:
                    age = int(age) 
                    break
                except ValueError:
                    print("Invalid age! Please enter a valid number.")

            while True:
                grade = input("Enter your grade: ").lower()
                if grade in valid_grades:
                    break
                else:
                    print("Invalid grade! Use a, b, or c.")

            self.c.execute("""INSERT INTO students (Name, Age, Grade) 
                            VALUES (?, ?, ?)""", 
                        (name.capitalize(), age, grade.upper()))
        
        self.connector.commit()
        print(f"{num_students} student(s) added successfully!")


    def DisplayTable(self, students):
        print("-" * 43)
        print(f"| {'ID':<5} | {'Name':<15} | {'Age':<5} | {'Grade':<5} |")
        print("-" * 43)

        for student in students:
            print(f"| {student[0]:<5} | {student[1]:<15} | {student[2]:<5} | {student[3]:<5} |")
            print("-" * 43)

    def ShowStudents(self):
        self.c.execute("SELECT * FROM students")
        students = self.c.fetchall()
        if students:
            self.DisplayTable(students)
        else:
            print("No students found.")

    def StudentsA(self):
        self.c.execute("SELECT * FROM students WHERE Grade = ?", ("A",))
        students = self.c.fetchall()
        if students:
            self.DisplayTable(students)
        else:
            print("No students with Grade 'A' found.")

    def Close(self):
        self.connector.close()

if __name__ == "__main__":
    sql = MySQL()

    while True:
        print("\n1. Add Student\n2. Show Students\n3. Grade 'A' Students\n4. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            sql.InsertDT()
        elif choice == '2':
            sql.ShowStudents()
        elif choice == '3':
            sql.StudentsA()
        elif choice == '4':
            sql.Close()
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")
