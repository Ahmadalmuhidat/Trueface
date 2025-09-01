class Lecture:
  def __init__(
    self, class_id: str, subject_area: str, catalog_nbr: str = None,
    academic_career: str = None, course: str = None, offering_nbr: str = None,
    start_time: str = None, end_time: str = None, section: str = None,
    component: str = None, campus: str = None, instructor_id: str = None,
    instructor_type: str = None, day: str = None
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
    self.instructor_id = instructor_id
    self.instructor_type = instructor_type
    self.day = day