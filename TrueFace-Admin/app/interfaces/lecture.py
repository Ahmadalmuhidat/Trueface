class Lecture:
  def __init__(
    self, class_id, subject_area, catalog_nbr = None, academic_career = None,
    course= None, offering_nbr = None, start_time = None, end_time = None, section = None,
    component = None, campus = None, instructor_id = None, instructor_type = None, day = None
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