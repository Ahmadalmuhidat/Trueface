from app.interfaces.instructor import Instructor

class Lecture:
  def __init__(
    self, class_id: str, subject_area: str, catalog_nbr: str = None,
    academic_career: str = None, course: str = None, offering_nbr: str = None,
    start_time: str = None, end_time: str = None, section: str = None,
    component: str = None, campus: str = None, instructor: Instructor = None, day: str = None
  ):
    self.lecture_id = class_id
    self.subject_area = subject_area
    self.catalog_nbr = catalog_nbr
    self.academic_career = academic_career
    self.Course = course
    self.offering_nbr = offering_nbr
    self.start_time = start_time
    self.end_time = end_time
    self.section = section
    self.component = component
    self.campus = campus
    self.instructor = instructor
    self.day = day

    self._students = []