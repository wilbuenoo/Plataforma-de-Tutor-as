class TutoringSession:
    def __init__(self, tutor_name, subject, date, time):
        self.tutor_name = tutor_name
        self.subject = subject
        self.date = date
        self.time = time
        self.students = []

    def enroll_student(self, student_data):
        self.students.append(student_data)