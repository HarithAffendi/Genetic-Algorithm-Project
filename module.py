class Course:
  course_code: str
  department_code: str
  duration_hours: int
  enrolled_students: set[str]

  def __init__(self, course_code: str, department_code: str, duration_hours: int, enrolled_students: set[str]):
    self.course_code = course_code
    self.department_code = department_code
    self.duration_hours = duration_hours
    self.enrolled_students = enrolled_students

  def __eq__(self, other):
    return isinstance(other, Course) and self.course_code == other.course_code

  def __hash__(self):
    return hash(self.course_code)

  def __str__(self):
    return f"{self.course_code}"

  def __repr__(self):
    return f"{self.course_code}"