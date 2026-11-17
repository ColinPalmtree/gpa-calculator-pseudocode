# models.py - Pseudocode

**Purpose:** This file has the 3 main classes, Course, Semester, and Student. It also handles calculating GPA and keeping track of credits.

A student has multiple semesters, and each semester has multiple courses.

Quality points = grade points * credits

GPA = total quality points / total credits

### Functions

**validate_credits(credits)**
- Try to convert credits to an integer
- If it doesn't work, raise InvalidCreditsErr
- If credits are less than 1 or more than 6, raise InvalidCreditsErr
- Otherwise return credits

**calculate_gpa(points, credits)**
- If credits = 0, return None because you can't divide by 0
- Otherwise return points / credits

### Class Course

**Constructor(name, credits, grade)**
- Remove extra spaces from the name
- If the name is empty, raise ValueError
- Save the course name
- Check credits using validate_credits
- Convert the grade into a letter using parse_grade

**set_grade(grade)**
- Update the letter grade using parse_grade

**grade_points()**
- Return the number of points the letter grade is worth

**quality_points()**
- Return grade points * credits

**earned_credits()**
- If the grade is passing, return the credits
- Otherwise return 0 since an F doesn't earn credits

**to_record()**
- Return the course name, credits, and letter grade as a tuple

**\_\_str\_\_()**
- Return the course information as a string like "Math (3 cr) - A"

### Class Semester

**Constructor(term_name)**
- Remove extra spaces from the semester name
- If the name is empty, raise ValueError
- Save the semester name
- Create an empty list for courses

**find_course(course_name)**
- Loop through all courses in the semester
- Compare the course names ignoring capitalization and extra spaces
- If a match is found, return that course
- If nothing matches, return None

**add_course(course)**
- Check if the course already exists using find_course
- If it does, raise DuplicateCourseErr
- Otherwise add the course to the list

**remove_course(course_name)**
- Find the course
- If it doesn't exist, raise CourseNotFoundErr
- Otherwise remove it and return the course

**total_credits()**
- Start total at 0
- Loop through the courses and add up their credits
- Return total

**quality_points()**
- Start total at 0
- Go through every course and add its quality points
- Return total

**earned_credits()**
- Start total at 0
- Add up the earned credits from every course
- Return total

**gpa()**
- Use calculate_gpa with the semester's total quality points and credits
- Return the GPA

### Class Student

**Constructor(name)**
- Remove extra spaces from the name
- If it's blank, just use "Student"
- Save the name
- Create an empty list for semesters

**find_semester(term_name)**
- Go through the semesters
- Compare the names ignoring capitalization
- If there's a match, return that semester
- Otherwise return None

**add_semester(term_name)**
- Check if that semester already exists
- If it does, raise DuplicateSemesterErr
- Otherwise create a new Semester
- Add it to the list and return it

**remove_semester(term_name)**
- Find the semester
- If it doesn't exist, raise SemesterNotFoundErr
- Otherwise remove it from the list and return it

**all_courses()**
- Go through every semester
- Get all the courses from each one
- Put them into one list and return it

**total_credits()**
- Add up the total credits from every semester
- Return total

**quality_points()**
- Add up the quality points from every semester
- Return total

**earned_credits()**
- Add up the earned credits from every semester
- Return total

**cumulative_gpa()**
- Calculate GPA using the student's total quality points and total credits
- Return the result

**what_if_gpa(planned)**
- This lets the student see what their GPA would be with additional grades
- Start with their current quality points and credits
- Go through each planned course
- Multiply the grade points by the credits and add that to total points
- Add the planned credits to total credits
- Calculate the new GPA and return it

**standing()**
- Get the student's cumulative GPA
- If there aren't any grades yet, return "No grades yet"
- If GPA is below 2.0, return "Below 2.0 - could be put on academic probation"
- If GPA is 3.5 or higher, return "Good standing (Dean's List range)"
- Otherwise return "Good standing"
