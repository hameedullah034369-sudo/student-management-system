import csv
import os
from typing import Dict, Optional


class Student:
    """Represents a single student entity with type safety."""

    def __init__(self, student_id: str, name: str, age: int, grade: str):
        self.id = student_id
        self.name = name
        self.age = age
        self.grade = grade

    def to_dict(self) -> Dict[str, str]:
        """Converts object data to a dictionary format for CSV writing."""
        return {
            "id": self.id,
            "name": self.name,
            "age": str(self.age),
            "grade": self.grade,
        }


class StudentManager:
    """Handles all CRUD (Create, Read, Update, Delete) operations using a CSV file."""

    def __init__(self, filename: str = "students.csv"):
        self.filename = filename
        self.headers = ["id", "name", "age", "grade"]
        self._initialize_csv()

    def _initialize_csv(self):
        """Creates the CSV file with headers if it doesn't exist yet."""
        if not os.path.exists(self.filename):
            with open(
                self.filename, mode="w", newline="", encoding="utf-8"
            ) as file:
                writer = csv.DictWriter(file, fieldnames=self.headers)
                writer.writeheader()

    def load_all(self) -> Dict[str, Student]:
        """Reads the CSV and loads records into an in-memory dictionary for fast lookup."""
        students = {}
        if not os.path.exists(self.filename):
            return students

        with open(self.filename, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                students[row["id"]] = Student(
                    student_id=row["id"],
                    name=row["name"],
                    age=int(row["age"]),
                    grade=row["grade"],
                )
        return students

    def _save_all(self, students: Dict[str, Student]):
        """Overwrites the CSV file with the updated in-memory dictionary data."""
        with open(self.filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            writer.writeheader()
            for student in students.values():
                writer.writerow(student.to_dict())

    def add_student(self, student: Student) -> bool:
        """Adds a new student if the ID doesn't already exist."""
        students = self.load_all()
        if student.id in students:
            return False  # Duplicate ID error

        students[student.id] = student
        self._save_all(students)
        return True

    def get_student(self, student_id: str) -> Optional[Student]:
        """Searches for a single student by their unique ID."""
        students = self.load_all()
        return students.get(student_id)

    def update_student(
        self,
        student_id: str,
        name: Optional[str] = None,
        age: Optional[int] = None,
        grade: Optional[str] = None,
    ) -> bool:
        """Updates specific fields of an existing student."""
        students = self.load_all()
        if student_id not in students:
            return False

        student = students[student_id]
        if name:
            student.name = name
        if age:
            student.age = age
        if grade:
            student.grade = grade

        self._save_all(students)
        return True

    def delete_student(self, student_id: str) -> bool:
        """Removes a student record completely from the CSV."""
        students = self.load_all()
        if student_id not in students:
            return False

        del students[student_id]
        self._save_all(students)
        return True


def main():
    manager = StudentManager()

    while True:
        print("\n=== Student Management Portal ===")
        print("1. Add Student (Teacher)")
        print("2. Update Student (Teacher)")
        print("3. Delete Student (Teacher)")
        print("4. Search Student by ID (Teacher/Parent)")
        print("5. Display All Students (Teacher/Parent)")
        print("6. Exit")

        choice = input("\nSelect an option (1-6): ").strip()

        if choice == "1":
            print("\n--- Add New Student ---")
            sid = input("Enter Student ID: ").strip()
            name = input("Enter Name: ").strip()
            try:
                age = int(input("Enter Age: ").strip())
            except ValueError:
                print("✗ Error: Age must be a number.")
                continue
            grade = input("Enter Grade/Class: ").strip()

            new_student = Student(sid, name, age, grade)
            if manager.add_student(new_student):
                print("✓ Student added successfully!")
            else:
                print("✗ Error: A student with this ID already exists.")

        elif choice == "2":
            print("\n--- Update Student Record ---")
            sid = input("Enter Student ID to update: ").strip()

            student = manager.get_student(sid)
            if not student:
                print("✗ Error: Student record not found.")
                continue

            print(f"Found: {student.name} (Grade: {student.grade})")
            print("Leave blank and press Enter to keep current value.")

            new_name = input(f"New Name [{student.name}]: ").strip() or None

            new_age_input = input(f"New Age [{student.age}]: ").strip()
            new_age = None
            if new_age_input:
                try:
                    new_age = int(new_age_input)
                except ValueError:
                    print("✗ Error: Age must be a number. Skipping age update.")

            new_grade = input(f"New Grade [{student.grade}]: ").strip() or None

            if manager.update_student(
                sid, name=new_name, age=new_age, grade=new_grade
            ):
                print("✓ Student record updated successfully!")
            else:
                print("✗ Error: Could not update record.")

        elif choice == "3":
            print("\n--- Delete Student Record ---")
            sid = input("Enter Student ID to delete: ").strip()

            confirm = (
                input(
                    f"Are you sure you want to delete student {sid}? (yes/no): "
                )
                .lower()
                .strip()
            )
            if confirm == "yes":
                if manager.delete_student(sid):
                    print("✓ Student record permanently deleted.")
                else:
                    print("✗ Error: Student record not found.")
            else:
                print("Deletion cancelled.")

        elif choice == "4":
            print("\n--- Search Student ---")
            sid = input("Enter Student ID to search: ").strip()
            student = manager.get_student(sid)
            if student:
                print("\n[Record Found]")
                print(f"ID:     {student.id}")
                print(f"Name:   {student.name}")
                print(f"Age:    {student.age}")
                print(f"Grade:  {student.grade}")
            else:
                print("✗ Student record not found.")

        elif choice == "5":
            print("\n--- All Student Records ---")
            all_students = manager.load_all()
            if not all_students:
                print("No records found in the database.")
            else:
                print(
                    f"{'ID':<10} | {'Name':<20} | {'Age':<5} | {'Grade':<10}"
                )
                print("-" * 55)
                for s in all_students.values():
                    print(
                        f"{s.id:<10} | {s.name:<20} | {s.age:<5} | {s.grade:<10}"
                    )

        elif choice == "6":
            print("\nThank you for using the portal. Goodbye!")
            break

        else:
            print(
                "✗ Invalid selection. Please choose a number between 1 and 6."
            )


if __name__ == "__main__":
    main()