from tortoise.contrib.pydantic.creator import pydantic_model_creator

from .models import (
    CourseModel,
    DepartmentModel,
    EnrollmentModel,
    InstructorModel,
    OfficeModel,
    StudentModel,
)

Student = pydantic_model_creator(StudentModel, name="Student")
StudentIn = pydantic_model_creator(StudentModel, name="StudentIn", exclude_readonly=True)

Instructor = pydantic_model_creator(InstructorModel, name="Instructor")
InstructorIn = pydantic_model_creator(InstructorModel, name="InstructorIn", exclude_readonly=True)

Office = pydantic_model_creator(OfficeModel, name="Office")
OfficeIn = pydantic_model_creator(OfficeModel, name="OfficeIn", exclude_readonly=True)

Department = pydantic_model_creator(DepartmentModel, name="Department")
DepartmentIn = pydantic_model_creator(DepartmentModel, name="DepartmentIn", exclude_readonly=True)

Course = pydantic_model_creator(CourseModel, name="Course")
CourseIn = pydantic_model_creator(CourseModel, name="CourseIn", exclude_readonly=True)

Enrollment = pydantic_model_creator(EnrollmentModel, name="Enrollment")
EnrollmentIn = pydantic_model_creator(EnrollmentModel, name="EnrollmentIn", exclude_readonly=True)
