class Student:

    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades_hw = {}

    def add_courses(self, course_name):
        self.courses_in_progress.append(course_name)

    def add_finished_courses(self, course_name):
        self.finished_courses.append(course_name)

    def rate_lecturer(self, lecturer, course, grade):
        if isinstance(lecturer,
                      Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def count_avg_mark_hw(self):
        avg_mark_hw = []
        for k, v in self.grades_hw.items():
            avg_mark_hw += v
        return round(sum(avg_mark_hw) / len(avg_mark_hw), 1)

    def __str__(self):
        result = f'''Имя: {self.name}
Фамилия: {self.surname}
Средняя оценка за домашние задания {self.count_avg_mark_hw()}
Курсы в процессе изучения: {', '.join(self.courses_in_progress)}
Зввершенные курсы: {', '.join(self.finished_courses)}'''
        return result

    def __ge__(self, other):
        if isinstance(other, Student):
            self_avg_mark_hw = self.count_avg_mark_hw()
            other_avg_mark_hw = other.count_avg_mark_hw()
            return self_avg_mark_hw >= other_avg_mark_hw
        else:
            return 'Ошибка'


class Mentor:

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):

    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def count_avg_mark_lectures(self):
        avg_mark_lectures = []
        for k, v in self.grades.items():
            avg_mark_lectures += v
        return round(sum(avg_mark_lectures) / len(avg_mark_lectures), 1)

    def __str__(self):
        result = f'''Имя: {self.name}
Фамилия: {self.surname}
Средняя оценка за лкеции: {self.count_avg_mark_lectures()}'''
        return result

    def __ge__(self, other):
        if isinstance(other, Lecturer):
            self_avg_mark_lectures = self.count_avg_mark_lectures()
            other_avg_mark_lectures = other.count_avg_mark_lectures()
            return self_avg_mark_lectures >= other_avg_mark_lectures
        else:
            return 'Ошибка'


class Reviewer(Mentor):

    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in student.courses_in_progress:
            if course in student.grades_hw:
                student.grades_hw[course] += [grade]
            else:
                student.grades_hw[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        result = f'''Имя: {self.name}
Фамилия: {self.surname}'''
        return result


def count_avg_mark_course_hw(students, course):
    result = []
    for student in students:
        for k, v in student.grades_hw.items():
            if k == course:
                result += v
    result = round(sum(result)/len(result), 1)
    return result


def count_avg_mark_course_lecture(lecturers, course):
    result = []
    for lecturer in lecturers:
        for k, v in lecturer.grades.items():
            if k == course:
                result += v
    result = round(sum(result)/len(result), 1)
    return result


# ----------------------------------------------------------------------------------------------------------

lecturer_1 = Lecturer('John', 'Smith')
lecturer_1.courses_attached = ['math', 'russ']

lecturer_2 = Lecturer('Rose', 'First')
lecturer_2.courses_attached = ['math', 'russ']

student_1 = Student('Ivan', 'Ivanov', 'male')
student_1.add_courses('math')
student_1.add_courses('geom')
student_1.add_finished_courses('russ')
student_1.add_finished_courses('litr')
student_1.rate_lecturer(lecturer_1, 'math', 5)
student_1.rate_lecturer(lecturer_2, 'math', 4)

student_2 = Student('Elena', 'Ivanova', 'female')
student_2.add_courses('russ')
student_2.add_courses('math')
student_2.rate_lecturer(lecturer_1, 'russ', 4)
student_2.rate_lecturer(lecturer_2, 'russ', 4)

reviewer_1 = Reviewer('Peter', 'Petrov')
reviewer_1.rate_hw(student_1, 'math', 5)
reviewer_1.rate_hw(student_1, 'geom', 4)
reviewer_1.rate_hw(student_2, 'russ', 4)
reviewer_1.rate_hw(student_2, 'math', 4)

reviewer_2 = Reviewer('Mike', 'Sidorov')
reviewer_2.rate_hw(student_1, 'math', 3)
reviewer_2.rate_hw(student_1, 'geom', 3)
reviewer_2.rate_hw(student_2, 'russ', 3)
reviewer_2.rate_hw(student_2, 'math', 3)

print('student_1:')
print(student_1)
print('student_2:')
print(student_2)
print('student_1 >= student_2:', student_1 >= student_2)
print()
print('reviewer_1:')
print(reviewer_1)
print('reviewer_2:')
print(reviewer_2)
print()
print('lecturer_1:')
print(lecturer_1)
print('lecturer_2:')
print(lecturer_2)
print('lecturer_1 >= lecturer_2:', lecturer_1 >= lecturer_2)


print()
students_list = [student_1, student_2]
print("count_avg_mark_course_hw(students_list, 'math'):")
print(count_avg_mark_course_hw(students_list, 'math'))

print()
lecturers_list = [lecturer_1, lecturer_2]
print("count_avg_mark_course_lecture(lecturers_list, 'russ'):")
print(count_avg_mark_course_lecture(lecturers_list, 'russ'))

