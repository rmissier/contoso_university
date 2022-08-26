from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from .routers import course, department, enrollment, instructor, office, student

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(course.router, prefix="/courses", tags=["Courses"])
app.include_router(department.router, prefix="/departments", tags=["Departments"])
app.include_router(enrollment.router, prefix="/enrollments", tags=["Enrollments"])
app.include_router(instructor.router, prefix="/instructors", tags=["Instructors"])
app.include_router(office.router, prefix="/offices", tags=["Offices"])
app.include_router(student.router, prefix="/students", tags=["Students"])


register_tortoise(
    app=app,
    db_url="sqlite://./contoso.sqlite3",
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
