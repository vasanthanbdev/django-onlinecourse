import sys
from django.utils.timezone import now
try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

from django.conf import settings
import uuid


# Instructor model
class Instructor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_time = models.BooleanField(default=True)
    total_learners = models.IntegerField()

    def __str__(self):
        return self.user.username


STUDENT = 'student'
DEVELOPER = 'developer'
DATA_SCIENTIST = 'data_scientist'
DATABASE_ADMIN = 'dba'
OCCUPATION_CHOICES = [
    (STUDENT, 'Student'),
    (DEVELOPER, 'Developer'),
    (DATA_SCIENTIST, 'Data Scientist'),
    (DATABASE_ADMIN, 'Database Admin')
]


# Learner model
class Learner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    occupation = models.CharField(null=False, max_length=20, choices=OCCUPATION_CHOICES, default=STUDENT)
    social_link = models.URLField(max_length=200, null=True)

    def __str__(self):
        return self.user.username + " " + self.occupation


# Course model
class Course(models.Model):
    name = models.CharField(null=False, max_length=30, default='online course')
    image = models.ImageField(upload_to='course_images/')
    description = models.CharField(max_length=1000)
    pub_date = models.DateField(null=True)
    instructors = models.ManyToManyField(Instructor)
    learners = models.ManyToManyField(Learner, through='Enrollment')
    total_enrollment = models.IntegerField(default=0)
    is_enrolled = False

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description


# Lesson model
class Lesson(models.Model):
    title = models.CharField(max_length=200, default="title")
    order = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lesson")
    content = models.TextField()


AUDIT = 'audit'
HONOR = 'honor'
BETA = 'BETA'
COURSE_MODES = [
    (AUDIT, 'Audit'),
    (HONOR, 'Honor'),
    (BETA, 'BETA')
]

# Enrollment model
class Enrollment(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name="enrollment")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollment")
    date_enrolled = models.DateField(default=now)
    mode = models.CharField(max_length=5, choices=COURSE_MODES, default=AUDIT)
    rating = models.FloatField(default=5.0)


# Question Model
class Question(models.Model):
    Lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="question")
    content = models.CharField(max_length=200)
    grade = models.IntegerField(default=50)

    def __str__(self):
        return "Question: " + self.content
    
    # method to calculate if the learner gets the score of the question
    def is_get_score(self, selected_ids):
        all_answers = self.choices.filter(is_correct=True).count()
        selected_correct = self.choices.filter(is_correct=True, id__in=selected_ids).count()
        if all_answers == selected_correct:
            return True
        else:
            return False
        

# Choice Model
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    content = models.TextField()
    is_correct = models.BooleanField(default=False)
        
        
# Submission Model
class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name="submission")
    choices = models.ManyToManyField(Choice)
