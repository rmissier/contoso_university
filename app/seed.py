import asyncio
from datetime import datetime

from tortoise import Tortoise, run_async

from .models import (
    CourseModel,
    DepartmentModel,
    EnrollmentModel,
    Grade,
    InstructorModel,
    OfficeModel,
    StudentModel,
)


async def init_db():
    config = {
        "connections": {
            "default": {
                "engine": "tortoise.backends.sqlite",
                "credentials": {"file_path": "./contoso.sqlite3"},
            }
        },
        "apps": {"models": {"models": ["app.models"], "default_connection": "default"}},
        "use_tz": False,
        "timezone": "UTC",
    }
    await Tortoise.init(config)
    await Tortoise.generate_schemas()


async def seed_students():
    if await StudentModel.all().count() > 0:
        return
    students = [
        StudentModel.create(
            first_name="Carson", last_name="Alexander", enrollment_date=datetime(2016, 9, 1)
        ),
        StudentModel.create(
            first_name="Meredith", last_name="Alonso", enrollment_date=datetime(2018, 9, 1)
        ),
        StudentModel.create(
            first_name="Arturo", last_name="Anand", enrollment_date=datetime(2019, 9, 1)
        ),
        StudentModel.create(
            first_name="Gytis", last_name="Barzdukas", enrollment_date=datetime(2018, 9, 1)
        ),
        StudentModel.create(first_name="Yan", last_name="Li", enrollment_date=datetime(2018, 9, 1)),
        StudentModel.create(
            first_name="Peggy", last_name="Justice", enrollment_date=datetime(2017, 9, 1)
        ),
        StudentModel.create(
            first_name="Laura", last_name="Norman", enrollment_date=datetime(2017, 9, 1)
        ),
        StudentModel.create(
            first_name="Nino", last_name="Olivetto", enrollment_date=datetime(2011, 9, 1)
        ),
    ]
    await asyncio.gather(*students)


async def seed_instructors():
    if await InstructorModel.all().count() > 0:
        return
    instructors = [
        InstructorModel.create(
            first_name="Kim", last_name="Abercrombie", hire_date=datetime(1995, 3, 11)
        ),
        InstructorModel.create(
            first_name="Fadi", last_name="Fakhouri", hire_date=datetime(2002, 7, 6)
        ),
        InstructorModel.create(
            first_name="Roger", last_name="Harui", hire_date=datetime(1998, 7, 1)
        ),
        InstructorModel.create(
            first_name="Candace", last_name="Kapoor", hire_date=datetime(2001, 1, 15)
        ),
        InstructorModel.create(
            first_name="Roger", last_name="Zheng", hire_date=datetime(2004, 2, 12)
        ),
    ]
    await asyncio.gather(*instructors)


async def seed_offices():
    if await OfficeModel.all().count() > 0:
        return
    offices = [
        OfficeModel.create(
            instructor=await InstructorModel.get(last_name="Fakhouri"), location="Smith 17"
        ),
        OfficeModel.create(
            instructor=await InstructorModel.get(last_name="Harui"), location="Gowan 27"
        ),
        OfficeModel.create(
            instructor=await InstructorModel.get(last_name="Kapoor"),
            location="Thompson 304",
        ),
    ]
    await asyncio.gather(*offices)


async def seed_departments():
    if await DepartmentModel.all().count() > 0:
        return
    departments = [
        DepartmentModel.create(
            name="English",
            budget=350_000,
            start_date=datetime(2007, 9, 1),
            administrator=await InstructorModel.get(last_name="Abercrombie"),
        ),
        DepartmentModel.create(
            name="Mathematics",
            budget=100_000,
            start_date=datetime(2007, 9, 1),
            administrator=await InstructorModel.get(last_name="Fakhouri"),
        ),
        DepartmentModel.create(
            name="Engineering",
            budget=350_000,
            start_date=datetime(2007, 9, 1),
            administrator=await InstructorModel.get(last_name="Harui"),
        ),
        DepartmentModel.create(
            name="Economics",
            budget=100_000,
            start_date=datetime(2007, 9, 1),
            administrator=await InstructorModel.get(last_name="Kapoor"),
        ),
    ]
    await asyncio.gather(*departments)


async def seed_courses():
    if await CourseModel.all().count() > 0:
        return
    course = await CourseModel.create(
        number=1050,
        title="Chemistry",
        credits=3,
        department=await DepartmentModel.get(name="Engineering"),
    )
    await course.instructors.add(await InstructorModel.get(last_name="Kapoor"))
    await course.instructors.add(await InstructorModel.get(last_name="Harui"))
    course = await CourseModel.create(
        number=4022,
        title="Microeconomics",
        credits=3,
        department=await DepartmentModel.get(name="Economics"),
    )
    await course.instructors.add(await InstructorModel.get(last_name="Zheng"))
    course = await CourseModel.create(
        number=4041,
        title="Macroeconomics",
        credits=3,
        department=await DepartmentModel.get(name="Economics"),
    )
    await course.instructors.add(await InstructorModel.get(last_name="Zheng"))
    course = await CourseModel.create(
        number=1045,
        title="Calculus",
        credits=4,
        department=await DepartmentModel.get(name="Mathematics"),
    )
    await course.instructors.add(await InstructorModel.get(last_name="Fakhouri"))
    course = await CourseModel.create(
        number=3141,
        title="Trigonometry",
        credits=4,
        department=await DepartmentModel.get(name="Mathematics"),
    )
    await course.instructors.add(await InstructorModel.get(last_name="Harui"))
    course = await CourseModel.create(
        number=2021,
        title="Composition",
        credits=3,
        department=await DepartmentModel.get(name="English"),
    )
    await course.instructors.add(await InstructorModel.get(last_name="Abercrombie"))
    course = await CourseModel.create(
        number=2042,
        title="Literature",
        credits=3,
        department=await DepartmentModel.get(name="English"),
    )
    await course.instructors.add(await InstructorModel.get(last_name="Abercrombie"))


async def seed_enrollments():
    alexander = await StudentModel.get(last_name="Alexander")
    alonso = await StudentModel.get(last_name="Alonso")
    anand = await StudentModel.get(last_name="Anand")
    barzdukas = await StudentModel.get(last_name="Barzdukas")
    li = await StudentModel.get(last_name="Li")
    justice = await StudentModel.get(last_name="Justice")

    calculus = await CourseModel.get(title="Calculus")
    chemistry = await CourseModel.get(title="Chemistry")
    composition = await CourseModel.get(title="Composition")
    literature = await CourseModel.get(title="Literature")
    macroeconomics = await CourseModel.get(title="Macroeconomics")
    microeconomics = await CourseModel.get(title="Microeconomics")
    trigonometry = await CourseModel.get(title="Trigonometry")

    await EnrollmentModel.create(student=alexander, course=chemistry, grade=Grade.A)
    await EnrollmentModel.create(student=alexander, course=microeconomics, grade=Grade.C)
    await EnrollmentModel.create(student=alexander, course=macroeconomics, grade=Grade.B)
    await EnrollmentModel.create(student=alonso, course=calculus, grade=Grade.B)
    await EnrollmentModel.create(student=alonso, course=trigonometry, grade=Grade.B)
    await EnrollmentModel.create(student=alonso, course=composition, grade=Grade.B)
    await EnrollmentModel.create(student=anand, course=chemistry, grade=Grade.X)
    await EnrollmentModel.create(student=anand, course=microeconomics, grade=Grade.B)
    await EnrollmentModel.create(student=barzdukas, course=chemistry, grade=Grade.B)
    await EnrollmentModel.create(student=li, course=composition, grade=Grade.B)
    await EnrollmentModel.create(student=justice, course=literature, grade=Grade.B)


async def main():
    await init_db()
    await seed_students()
    await seed_instructors()
    await seed_offices()
    await seed_departments()
    await seed_courses()
    await seed_enrollments()


if __name__ == "__main__":
    run_async(main())
