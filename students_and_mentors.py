class Lecturers(type):
    instances = []

    def __call__(cls, *args, **kwargs):
        instance = super(Lecturers, cls).__call__(*args, **kwargs)
        cls.instances.append(instance)

        return instance


class Students(type):
    instances = []

    def __call__(cls, *args, **kwargs):
        instance = super(Students, cls).__call__(*args, **kwargs)
        cls.instances.append(instance)

        return instance


class Student(metaclass=Students):

    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)

    def rate_lec(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress or course in self.finished_courses \
                and course in lecturer.courses_attached:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:

            return 'Ошибка'

    def __mid_grades(self):
        sum_grades = 0
        counter = 0
        for grades in self.grades.values():
            for grade in grades:
                counter += 1
                sum_grades += grade
        mid_grade = sum_grades/counter

        return mid_grade

    def __str__(self):
        name = self.name
        surname = self.surname

        return f"Имя: {name}\nФамилия: {surname}\nСредняя оценка за домашние задания: {self.__mid_grades()}\n" \
               f"Курсы в процессе изучения: {', '.join(self.courses_in_progress)}\n" \
               f"Завершенные курсы: {', '.join(self.finished_courses)}"

    def __le__(self, other):
        if not isinstance(other, Student):
            return "Ошибка"

        return self.__mid_grades() <= other.__mid_grades()

    def __lt__(self, other):
        if not isinstance(other, Student):
            return "Ошибка"

        return self.__mid_grades() < other.__mid_grades()


class Mentor:

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor, metaclass=Lecturers):

    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __mid_grades(self):
        sum_grades = 0
        counter = 0
        for grades in self.grades.values():
            for grade in grades:
                counter += 1
                sum_grades += grade
        mid_grade = sum_grades/counter

        return mid_grade

    def __str__(self):
        name = self.name
        surname = self.surname

        return f"Имя: {name}\nФамилия: {surname}\nСредняя оценка за лекции: {self.__mid_grades()}"

    def __le__(self, other):
        if not isinstance(other, Lecturer):
            return "Ошибка"

        return self.__mid_grades() <= other.__mid_grades()

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return "Ошибка"

        return self.__mid_grades() < other.__mid_grades()


class Reviewer(Mentor):

    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:

            return 'Ошибка'

    def __str__(self):
        name = self.name
        surname = self.surname

        return f"Имя: {name}\nФамилия: {surname}"


# Первый студент
best_student = Student('Piter', 'Parker', 'mail')
best_student.finished_courses += ['Git']
best_student.courses_in_progress += ['Python']
best_student.grades['Git'] = [10, 10, 10, 10, 10]
best_student.grades['Python'] = [10, 10]

# Второй студент
lose_student = Student('Eddie', 'Brock', 'mail')
lose_student.finished_courses += ['Git']
lose_student.courses_in_progress += ['Python']
lose_student.grades['Git'] = [5, 6, 7, 5, 2]
lose_student.grades['Python'] = [10, 3]

# Преподаватель
cool_reviewer = Reviewer('Cool', 'Reviewer')
cool_reviewer.courses_attached += ['Python']

# Выставили оценку первому студенту
cool_reviewer.rate_hw(best_student, 'Python', 9)

# Выставили оценку второму студенту
cool_reviewer.rate_hw(lose_student, 'Python', 5)

# Первый лектор
stan_lecturer = Lecturer('Stan', 'Lee')
stan_lecturer.courses_attached += ['Git', 'Python']

# Второй лектор
steve_lecturer = Lecturer('Steve', 'Ditko')
steve_lecturer.courses_attached += ['Git', 'Python']

# Первый студент выставил оценку Первому лектору
best_student.rate_lec(stan_lecturer, 'Git', 8)
best_student.rate_lec(stan_lecturer, 'Python', 2)

# Второй студент выставил оценку Второму лектору
lose_student.rate_lec(steve_lecturer, 'Git', 2)
lose_student.rate_lec(steve_lecturer, 'Python', 10)

# Выводим на экран всех участнков программы
print(best_student, lose_student, cool_reviewer, steve_lecturer, stan_lecturer, sep='\n \n')

# Сравниваем оценки студентов
print(best_student > lose_student)
print(best_student <= lose_student)

# Сравниваем оценки лекторов
print(steve_lecturer < stan_lecturer)
print(steve_lecturer >= stan_lecturer)


def mid_grades_students(students, course):
    """
    Функция для подсчета средней оценки за курс у всех студентов
    """
    counter = 0
    len_grades = 0
    for student in students:
        counter += sum(student.__dict__['grades'][course])
        len_grades += len(student.__dict__['grades'][course])

    return f"Средняя оценка за курс {course} у всех студентов: {counter / len_grades}"


def mid_grades_lecturers(lecturers, course):
    """
    Функция для подсчета средней оценки за курс у всех лекторов
    """
    counter = 0
    len_grades = 0
    for lecturer in lecturers:
        counter += sum(lecturer.__dict__['grades'][course])
        len_grades += len(lecturer.__dict__['grades'][course])

    return f"Средняя оценка за курс {course} у всех лекторов: {counter / len_grades}"


print(mid_grades_students(Students.instances, 'Git'))
print(mid_grades_lecturers(Lecturers.instances, 'Python'))
