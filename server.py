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


# @app.get("/api/v1/review_type_map")
# @stringify_exceptions
# async def get_review_type_map():
#     return {
#         "response": {review_type.value: review_type.name for review_type in ReviewType},
#         "status": "success",
#     }


# @app.get("/api/v1/courses_review_counts")
# @stringify_exceptions
# async def get_courses_review_counts():
#     course = courses.get_course(course)
#     s = AssimilScheduler(course, db=db)
#     return {
#         "response": s.get_courses_review_counts(),
#         "status": "success",
#     }


@app.get("/api/v1/health")
@stringify_exceptions
async def health():
    return {"response": "ok", "status": "success"}


@app.get("/api/v1/get_course/{course}")
@stringify_exceptions
async def get_course(course: str):
    c = courses.get_course(course)
    s = AssimilScheduler(c, db=db)
    next_review_lesson = next(s.review_generator(next_n=1))
    return {"response": c.to_json(next_review_lesson.priority), "status": "success"}


@app.get("/api/v1/courses")
@stringify_exceptions
async def list_courses():
    return {"response": courses.list_courses(), "status": "success"}


@app.get("/api/v1/percentages")
@stringify_exceptions
async def courses_percentages():
    response = {}
    for course in courses.list_courses():
        c = courses.get_course(course)
        s = AssimilScheduler(c, db=db)
        response[course] = s.get_course_percentage()
    return {"response": response, "status": "success"}

@app.get("/api/v1/review_counts")
@stringify_exceptions
async def review_counts():
    c = courses.get_course("french")
    s = AssimilScheduler(c, db=db)
    response = s.get_review_counts_by_date()
    return {"response": response, "status": "success"}





# @app.get("/api/v1/reviews/{course}")
# @stringify_exceptions
# async def get_all_reviews(course: str):
#     course = courses.get_course(course)
#     s = AssimilScheduler(course, db=db)
#     response = [
#         (datetime.strftime(review[0], "%Y-%m-%d"), review[2].name, review[1])
#         for review in s.get_all_reviews(course.name)
#     ]
#     return {"response": response, "status": "success"}


@app.get("/api/v1/next_review/{course}")
@stringify_exceptions
async def next_review(course: str):
    c = courses.get_course(course)
    s = AssimilScheduler(c, db=db)
    next_review_lesson = next(s.review_generator(next_n=1))
    return {"response": next_review_lesson.to_dict(), "status": "success"}


@app.get("/api/v1/complete_review/{course}")
@stringify_exceptions
async def complete_review(course: str):
    c = courses.get_course(course)
    s = AssimilScheduler(c, db=db)
    s.mark_as_done()
    return {"status": "success"}


@app.get("/api/v1/undo_review/{course}")
@stringify_exceptions
async def undo_review(course: str):
    c = courses.get_course(course)
    s = AssimilScheduler(c, db=db)
    s.undo_last_review()
    return {"status": "success"}


# query param ?next_n=4
# @app.get("/api/v1/next_reviews/{course}")
# @stringify_exceptions
# async def next_review(course: str, next_n: int = 4):
#     course = courses.get_course(course)
#     s = AssimilScheduler(course, db=db)
#     next_n = min(next_n, 100)
#     next_n = max(next_n, 1)
#     output = []
#     for review in s.review_generator(next_n=next_n):
#         if next_n <= 0:
#             break
#         output.append(review.to_dict())
#         next_n -= 1
#     return {"response": output, "status": "success"}


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def serve_home_page():
    headers = {
        "Cache-Control": "public, max-age=30, immutable",
    }
    return FileResponse("static/pages/home-page.html", headers=headers)


@app.get("/{course}")
async def serve_language_page():
    headers = {
        "Cache-Control": "public, max-age=30, immutable",
    }
    return FileResponse("static/pages/language-page.html", headers=headers)


@app.get("/favicon.ico")
async def serve_favicon():
    return FileResponse("static/favicon.ico")


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8080)
