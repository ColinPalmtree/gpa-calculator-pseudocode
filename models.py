# models.py
# the classes: Course, Semester, Student
#
# a Student has a list of Semesters, a semester has a list of courses
# gpa = total quality points / total credits
# quality points = grade points* credits

from errors import (InvalidCreditsErr, DuplicateCourseErr, DuplicateSemesterErr, CourseNotFoundErr, SemesterNotFoundErr)
from grades import letter_to_points, parse_grade, is_passing

Min_creds = 1
Max_creds = 6

def validate_credits(credits):
  try:
    credits = int(credits)
  except (ValueError, TypeError):
    raise InvalidCreditsErr(f"credits have to be a whole number, not '{credits}'")
  if credits <Min_creds or credits> Max_creds:
    raise InvalidCreditsErr(f"credits have to be {Min_creds}-{Max_creds}(you put {credits}")
  return credits

def calculate_gpa(points, credits):
  if credits == 0 :
    return None # can't divide by 0
  return points / credits
  
class Course:
  def __init__(self, name, credits, grade):
    name = str(name).strip()
    if name == "":
      raise ValueError("Course name can't be blank")
    self.name = name
    self.credits = validate_credits(credits)
    self.letter = parse_grade(grade)

  def set_grade(self, grade):
    self.letter = parse_grade(grade)

  def grade_points(self):
    return letter_to_points(self.letter)

  def quality_points(self):
    return self.grade_points() * self.credits

  def earned_credits(self):
    # you don't get the credits if you fail
    if is_passing(self.letter):
      return self.credits
    return 0

  def to_record(self):
    return (self.name, self.credits, self.letter)

  def __str__(self):
    return f"{self.name} ({self.credits} cr) - {self.letter}"
    
class Semester:
  def __init__(self, term_name):
    term_name = str(term_name).strip()
    if term_name == "":
      raise ValueError("Semester name can't be blank")
    self.term_name = term_name
    self.courses = []

  def find_course(self, course_name):
    target = course_name.strip().lower()
    for course in self.courses:
      if course.name.lower() == target: 
        return course
    return None

  def add_course(self, course):
    if self.find_course(course.name) is not None:
      raise DuplicateCourseErr(f"{course.name} is already in {self.term_name}")
    self.courses.append(course)
    
  def remove_course(self, course_name):
    course = self.find_course(course_name)
    if course is None:
      raise CourseNotFoundErr(f"No course called {course_name} in {self.term_name}")
    self.courses.remove(course)
    return course

  def total_credits(self):
    total = 0
    for course in self.courses:
      total += course.credits
    return total

  def quality_points(self):
    total = 0.0
    for course in self.courses:
      total += course.quality_points()
    return total

  def earned_credits(self):
    total = 0
    for course in self.courses:
      total += course.earned_credits()
    return total

  def gpa(self):
    return calculate_gpa(self.quality_points(), self.total_credits())

  def __str__(self):
    return f"{self.term_name} ({len(self.courses)} courses)"
    
class Student:
  def __init__(self, name):
    name = str(name).strip()
    if name == "":
      name = "Student"
    self.name = name
    self.semesters = []

  def find_semester(self,term_name):
    target = term_name.strip().lower()
    for semester in self.semesters:
      if semester.term_name.lower() == target: 
        return semester
    return None

  def add_semester(self, term_name):
    if self.find_semester(term_name) is not None:
      raise DuplicateSemesterErr(f"{term_name} already exists")
    semester = Semester(term_name)
    self.semesters.append(semester)
    return semester

  def remove_semester(self, term_name):
    semester = self.find_semester(term_name)
    if semester is None:
      raise SemesterNotFoundErr(f" no semester called {term_name}")
    self.semesters.remove(semester)
    return semester

  def all_courses(self):
    courses = []
    for semester in self.semesters:
      courses.extend(semester.courses)
    return courses

  def total_credits(self)
    total = 0
    for semester in self.semesters:
        total += semester.total_credits()
    return total

  def quality_points(self):
    total = 0.0
    for semester in self.semesters:
      total += semester.quality_points()
    return total

  def earned_credits(self):
    total = 0
    for semester in self.semesters:
      total += semester.earned_credits()
    return total

  def cumulative_gpa(self):
    return calculate_gpa(self.quality_points(), self.total_credits())

  def what_if_gpa(self, planned):
      # planned = list of (credits, letter) tuples for classes you haven't taken yet
      # returns the gpa you'd have after those classes
      points = self.quality_points()
      credits = self.total_credits()
      for planned_credits, letter in planned:
        points += letter_to_points(letter) * planned_credits
        credits += planned_credits
      return calculate_gpa(points, credits)

  def standing(self):
    gpa = self.cumulative_gpa()
    if gpa is None:
      return "No grades yet"
    if gpa < 2.0:
      return " Below 2.0 - could be put on academic probation"
    if gpa >= 3.5:
      return "Good standing (Dean's List range)"
    return "Good standing"
  

    
