import threading

from app.interfaces.lecture import Lecture
from typing import List
from app.helper.error_handler import error_handler

class Course:
  def __init__(
    self, course_id: str, title: str, credit: str, maximum_units: str,
    long_course_title: str, offering_nbr: str, academic_group: str,
    subject_area: str, catalog_nbr: str, campus: str,
    academic_organization: str, component: str
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

  @error_handler
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
  
  def search_leacture(self, term: str):
    return [lecture for lecture in self._lectures if term == lecture.lecture_id or term in lecture.subject_area]

  def get_lectures(self) -> List[Lecture]:
    return self._lectures

  def add_lecture(self, lecture: Lecture):
    self._lectures.append(lecture)

  def remove_lecture(self, lecture_id):
    self._lectures = [lecture for lecture in self._lectures if lecture.lecture_id != lecture_id]
