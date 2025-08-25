import threading

from app.interfaces.lecture import Lecture
from typing import List

class Course:
  def __init__(
    self, course_id, title, credit, maximum_units, long_course_title, offering_nbr,
    academic_group, subject_area, catalog_nbr, campus, academic_organization, component
  ):
    self.course_id = course_id
    self.title = title
    self.credit = credit
    self.maximum_units = maximum_units
    self.long_course_title = long_course_title
    self.offering_nbr = offering_nbr
    self.academic_group = academic_group
    self.subject_area = subject_area
    self.catalog_nbr = catalog_nbr
    self.campus = campus
    self.academic_organization = academic_organization
    self.component = component

    self._lectures = []
  
    threading.Thread(target=self.fetch_lectures).start()

  def fetch_lectures(self):
    from app.controllers.courses import get_lectures_by_course

    self._lectures.clear()

    for data in get_lectures_by_course(self):
      lecture_object = Lecture(
        data['ID'],
        data['SubjectArea'],
        data['CatalogNBR'],
        data['AcademicCareer'],
        data['Course'], 
        data['OfferingNBR'], 
        data['StartTime'],
        data['EndTime'], 
        data['Section'], 
        data['Component'], 
        data['Campus'], 
        data['Name'], 
        data['InstructorType']
      )
      self.add_lecture(lecture_object)

  def get_lectures(self) -> List[Lecture]:
    return self._lectures

  def add_lecture(self, lecture: Lecture):
    self._lectures.append(lecture)

  def remove_lecture(self, lecture_id):
    self._lectures = [lecture for lecture in self._lectures if lecture.lecture_id != lecture_id]
