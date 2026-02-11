import threading

from app.interfaces.lecture import Lecture
from app.interfaces.instructor import Instructor
from typing import List
from app.utils.error_handler import error_handler

class Course:
  def __init__(
    self, course_id: str, title: str, credit: str, maximum_units: str,
    long_course_title: str, offering_nbr: str, academic_group: str,
    subject_area: str, catalog_nbr: str, campus: str,
    academic_organization: str, component: str
  ) -> None:
    self.id = course_id
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

    self._lectures: list[Lecture] = []

    threading.Thread(target=self.fetch_lectures, daemon=True).start()

  @error_handler
  def fetch_lectures(self) -> None:
    from app.controllers.courses import CoursesController

    self._lectures.clear()

    for data in CoursesController().fetch_lectures_by_course(self):
      lecture_id = data.get('id')
      subject_area = data.get('subject_area')
      catalog_nbr = data.get('catalog_nbr')
      academic_career = data.get('academic_career')
      course_id = data.get('course')
      offering_nbr = data.get('offering_nbr')
      start_time = data.get('start_time')
      end_time = data.get('end_time')
      section = data.get('section')
      component = data.get('component')
      campus = data.get('campus')
      instructor_id = data.get('instructor_id')
      instructor_name = data.get('name')
      
      lecture_object = Lecture(
        lecture_id,
        subject_area,
        catalog_nbr,
        academic_career,
        course_id, 
        offering_nbr, 
        start_time,
        end_time, 
        section, 
        component, 
        campus,
        Instructor(
          instructor_id,
          instructor_name
        )
      )
      self.add_lecture(lecture_object)
  
  def search_lecture(self, term: str) -> List[Lecture]:
    return [lecture for lecture in self._lectures if term == lecture.lecture_id or term in lecture.subject_area]

  def get_lectures(self) -> List[Lecture]:
    return self._lectures

  def add_lecture(self, lecture: Lecture) -> None:
    self._lectures.append(lecture)

  def remove_lecture(self, lecture_id: str) -> None:
    self._lectures = [lecture for lecture in self._lectures if lecture.lecture_id != lecture_id]
