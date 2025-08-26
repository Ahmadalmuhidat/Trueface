from app.config.context import Context

CONTEXT = Context()

def get_all_lectures():
  lectures = []
  for course in CONTEXT.get_courses():
    course_lectures = course.get_lectures()
    lectures.extend(course_lectures)
  return lectures