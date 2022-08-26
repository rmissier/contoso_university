from enum import Enum

from tortoise import Tortoise, fields
from tortoise.models import Model


class StudentModel(Model):
    id = fields.IntField(pk=True)
    last_name = fields.CharField(max_length=50, null=False)
    first_name = fields.CharField(max_length=50, null=False)
    enrollment_date = fields.DateField(null=False)

    enrollments: fields.ReverseRelation["EnrollmentModel"]

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"StudentModel(first_name={self.first_name}, last_name={self.last_name})"


class InstructorModel(Model):
    id = fields.IntField(pk=True)
    last_name = fields.CharField(max_length=50, null=False)
    first_name = fields.CharField(max_length=50, null=False)
    hire_date = fields.DateField(null=False)

    course: fields.ReverseRelation["CourseModel"]
    office: fields.ReverseRelation["OfficeModel"]

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"InstructorModel(first_name={self.first_name}, last_name={self.last_name})"


class OfficeModel(Model):
    id = fields.IntField(pk=True)
    instructor: fields.ForeignKeyRelation[InstructorModel] = fields.ForeignKeyField(
        "models.InstructorModel",
        related_name="office",
        on_delete=fields.SET_NULL,
        index=True,
        null=True,
    )
    location = fields.CharField(max_length=200, null=False)

    def __str__(self):
        return f"OfficeModel(instructor={self.instructor}, location={self.location}"


class DepartmentModel(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, null=False)
    budget = fields.IntField(null=False)
    start_date = fields.DateField(null=False)
    administrator: fields.ForeignKeyRelation[InstructorModel] = fields.ForeignKeyField(
        "models.InstructorModel",
        on_delete=fields.SET_NULL,
        null=True,
    )

    courses: fields.ReverseRelation["CourseModel"]

    def __str__(self):
        return f"DepartmentModel(name={self.name})"


class CourseModel(Model):
    id = fields.IntField(pk=True)
    number = fields.IntField(null=False, unique=True)
    title = fields.CharField(max_length=50, null=False)
    credits = fields.IntField(null=False)
    department: fields.ForeignKeyRelation[DepartmentModel] = fields.ForeignKeyField(
        "models.DepartmentModel",
        related_name="courses",
        on_delete=fields.SET_NULL,
        null=True,
    )
    instructors: fields.ManyToManyRelation[InstructorModel] = fields.ManyToManyField(
        "models.InstructorModel",
        related_name="course",
    )

    enrollments: fields.ReverseRelation["EnrollmentModel"]

    def __str__(self):
        return f"CourseModel(id={self.id}, title={self.title}, credits={self.credits})"


class Grade(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    F = "F"
    X = "X"


class EnrollmentModel(Model):
    id = fields.IntField(pk=True)
    course: fields.ForeignKeyRelation[CourseModel] = fields.ForeignKeyField(
        "models.CourseModel",
        related_name="enrollments",
        on_delete=fields.SET_NULL,
        null=True,
    )
    student: fields.ForeignKeyRelation[StudentModel] = fields.ForeignKeyField(
        "models.StudentModel",
        related_name="enrollments",
        on_delete=fields.CASCADE,
        null=False,
    )
    grade: Grade = fields.CharEnumField(Grade, null=False, default=Grade.X)

    def __str__(self):
        return f"EnrollmentModel(course={self.course}, student={self.student})"


Tortoise.init_models(["app.models"], "models")
