class Person:
    def __init__(self, name: str, age: int):
        """Creates a new Person object with name and age

        Args:
            name (str): Person's name
            age (int): Person's age
        """
        self.name = name
        self.age = age

    def introduce(self) -> str:
        """Returns a string introducing the person's name and age

        Returns:
            str: String introducing this Person
        """
        return f"My name is {self.name} and I am {self.age} years old."


class Student(Person):
    def __init__(self, name: str, age: int, grade: str):
        """Creates Student with name and age (from person inheritence) and Student's letter grade

        Args:
            name (str): Student's name (from Person)
            age (int): Student's age
            grade (str): Student's current letter grade
        """
        super().__init__(name, age)
        self.grade = grade

    def study(self, hours: int) -> str:
        """Returns a string stating that this student has studied for a number of hours

        Args:
            hours (int): number of hours studied

        Returns:
            str: string stating that this student has studied for (hours) hours
        """
        return f"{self.name} studied for {hours} hours."

    def get_profile(self):
        """Returns a string of a Student's profile (name, age and grade)

        Returns:
            str: Student profile string
        """
        return f"Name: {self.name}\nAge: {self.age}\nGrade: {self.grade}"


class Teacher(Person):
    def __init__(self, name: str, age: int, subject: str):
        """Creates Teacher object with name and age (from person inheritence) and subject the Teacher teaches

        Args:
            name (str): Teacher's name (from Person)
            age (int): Teacher's age (from Person)
            subject (str): subject taught by the Teacher (math, science, art, etc.)
        """
        super().__init__(name, age)
        self.subject = subject

    def teach(self, topic: str) -> str:
        """Returns a string stating that the Teacher teaches about a topic in their subject

        Args:
            topic (str): what topic is being taught about (geometry topic in math subject, biology topic in science subject, etc.)

        Returns:
            str: string stating that the Teacher teaches about a topic in their subject
        """
        return f"{self.name} teaches about {topic} in {self.subject}."

    def grade_student(self, student: Student, grade: str):
        """Updates specified Student's grade

        Args:
            student (Student): Student object for which to change grade
            grade (str): new letter grade
        """
        student.grade = grade


##### TESTS BELOW #####

import unittest

# Person, Student, and Teacher imports commented out for testing in same file
# import Person
# import Student
# import Teacher


class TestPerson(unittest.TestCase):
    def setUp(self):
        self.person = Person("John Doe", 30)

    def test_introduce(self):
        msg = self.person.introduce()
        self.assertIn("30", msg)
        self.assertIn("John Doe", msg)


class TestStudent(unittest.TestCase):
    def setUp(self):
        self.student = Student("Jane Doe", 20, "A")

    def test_study(self):
        msg = self.student.study(5)
        self.assertIn("5", msg)
        self.assertIn("Jane Doe", msg)

    def test_get_profile(self):
        msg = self.student.get_profile()
        self.assertIn("Name: Jane Doe", msg)
        self.assertIn("Grade: A", msg)
        self.assertIn("Age: 20", msg)


class TestTeacher(unittest.TestCase):
    def setUp(self):
        self.teacher = Teacher("Bob Smith", 40, "Math")
        self.student = Student("Jane Doe", 20, "B")

    def test_teach(self):
        msg = self.teacher.teach("Calculus")
        self.assertIn("Calculus", msg)
        self.assertIn("Bob Smith", msg)

    def test_grade_student(self):
        self.assertEqual("B", self.student.grade)
        self.teacher.grade_student(self.student, "A")
        self.assertEqual("A", self.student.grade)


if __name__ == "__main__":
    unittest.main()
