from datetime import datetime
from functools import wraps

from uvicorn import run
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.db import DB
from src.schema import ReviewType
from src.courses import Courses
from src.scheduler import AssimilScheduler

app = FastAPI()
courses = Courses()
db = DB()


def stringify_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            return {"error": str(e), "status": "error"}

    return wrapper


@app.get("/api/v1/review_type_map")
@stringify_exceptions
async def get_review_type_map():
    return {
        "response": {review_type.value: review_type.name for review_type in ReviewType},
        "status": "success",
    }


@app.get("/api/v1/get_course/{course}")
@stringify_exceptions
async def get_course(course: str):
    course = courses.get_course(course)
    return {"response": course.to_json(), "status": "success"}


@app.get("/api/v1/courses")
@stringify_exceptions
async def list_courses():
    return {"response": courses.list_courses(), "status": "success"}


@app.get("/api/v1/reviews/{course}")
@stringify_exceptions
async def get_all_reviews(course: str):
    course = courses.get_course(course)
    s = AssimilScheduler(course, db=db)
    response = [
        (datetime.strftime(review[0], "%Y-%m-%d"), review[2].name, review[1])
        for review in s.get_all_reviews(course.name)
    ]
    return {"response": response, "status": "success"}


@app.get("/api/v1/next_review/{course}")
@stringify_exceptions
async def next_review(course: str):
    course = courses.get_course(course)
    s = AssimilScheduler(course, db=db)
    next_review_lesson = next(s.review_generator(next_n=1))
    return {"response": next_review_lesson.to_dict(), "status": "success"}


# query param ?next_n=4
@app.get("/api/v1/next_reviews/{course}")
@stringify_exceptions
async def next_review(course: str, next_n: int = 4):
    course = courses.get_course(course)
    s = AssimilScheduler(course, db=db)
    next_n = min(next_n, 100)
    next_n = max(next_n, 1)
    output = []
    for review in s.review_generator(next_n=next_n):
        if next_n <= 0:
            break
        output.append(review.to_dict())
        next_n -= 1
    return {"response": output, "status": "success"}


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def serve_index():
    return FileResponse("static/index.html")


@app.get("/favicon.ico")
async def serve_index():
    return FileResponse("static/favicon.ico")


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8080)
