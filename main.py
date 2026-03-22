Code required to create this platform using API
from fastapi import FastAPI, Query, Response, status
from pydantic import BaseModel, Field

app = FastAPI()

# ================= MODELS =================

class CourseCreate(BaseModel):
    title: str = Field(..., min_length=3)
    category: str
    price: int = Field(..., gt=0)
    rating: float = Field(..., ge=0, le=5)
    available: bool = True


class EnrollmentRequest(BaseModel):
    student_name: str
    course_id: int


# ================= DATA =================

courses = [
    {"id":1,"title":"Python Basics","category":"Programming","price":999,"rating":4.5,"available":True},
    {"id":2,"title":"FastAPI Development","category":"Programming","price":1499,"rating":4.7,"available":True},
    {"id":3,"title":"UI UX Design","category":"Design","price":1299,"rating":4.2,"available":False},
    {"id":4,"title":"Digital Marketing","category":"Marketing","price":899,"rating":4.1,"available":True}
]

enrollments = []
course_counter = 5


# ================= HELPERS =================

def find_course(course_id:int):
    for c in courses:
        if c["id"] == course_id:
            return c
    return None


# ================= DAY 1 =================

@app.get("/")
def home():
    return {"message":"Welcome to Online Course Platform, world of learning "}


@app.get("/courses")
def get_courses():
    return {"courses":courses,"total":len(courses)}


@app.get("/courses/summary")
def course_summary():

    available=[c for c in courses if c["available"]]
    unavailable=[c for c in courses if not c["available"]]

    return {
        "total_courses":len(courses),
        "available_courses":len(available),
        "unavailable_courses":len(unavailable)
    }


# ================= DAY 6 (FIXED ROUTES FIRST) =================

@app.get("/courses/search")
def search_course(keyword:str=Query(...)):

    results=[c for c in courses if keyword.lower() in c["title"].lower()]

    if not results:
        return {"message":"No courses found","results":[]}

    return {"results":results}


@app.get("/courses/sort")
def sort_courses(sort_by:str="price",order:str="asc"):

    reverse=(order=="desc")

    sorted_courses=sorted(courses,key=lambda c:c[sort_by],reverse=reverse)

    return {"courses":sorted_courses}


@app.get("/courses/page")
def courses_page(page:int=1,limit:int=2):

    start=(page-1)*limit
    end=start+limit

    return {
        "page":page,
        "courses":courses[start:end]
    }


@app.get("/courses/browse")
def browse_courses(
    category:str=Query(None),
    min_price:int=Query(None),
    max_price:int=Query(None)
):

    result=courses

    if category:
        result=[c for c in result if c["category"]==category]

    if min_price:
        result=[c for c in result if c["price"]>=min_price]

    if max_price:
        result=[c for c in result if c["price"]<=max_price]

    return {"courses":result}


# ================= DAY 4 CRUD =================

@app.post("/courses",status_code=201)
def add_course(data:CourseCreate):

    global course_counter

    for c in courses:
        if c["title"].lower()==data.title.lower():
            return {"error":"Course already exists"}

    new_course={
        "id":course_counter,
        "title":data.title,
        "category":data.category,
        "price":data.price,
        "rating":data.rating,
        "available":data.available
    }

    courses.append(new_course)
    course_counter+=1

    return {"message":"Course added","course":new_course}


@app.put("/courses/{course_id}")
def update_course(course_id:int,price:int=Query(None),available:bool=Query(None)):

    course=find_course(course_id)

    if not course:
        return {"error":"Course not found"}

    if price is not None:
        course["price"]=price

    if available is not None:
        course["available"]=available

    return {"message":"Course updated","course":course}


@app.delete("/courses/{course_id}")
def delete_course(course_id:int):

    course=find_course(course_id)

    if not course:
        return {"error":"Course not found"}

    courses.remove(course)

    return {"message":"Course deleted"}


# ================= VARIABLE ROUTE LAST =================

@app.get("/courses/{course_id}")
def get_course(course_id:int):

    course=find_course(course_id)

    if not course:
        return {"error":"Course not found"}

    return {"course":course}


# ================= DAY 5 WORKFLOW =================

@app.post("/enroll")
def enroll(data:EnrollmentRequest):

    course=find_course(data.course_id)

    if not course:
        return {"error":"Course not found"}

    if not course["available"]:
        return {"error":"Course not available"}

    enrollment={
        "student":data.student_name,
        "course":course["title"]
    }

    enrollments.append(enrollment)

    return {"message":"Enrollment successful","data":enrollment}


@app.get("/enrollments")
def get_enrollments():
    return {"enrollments":enrollments}


@app.get("/enrollments/search")
def search_enrollment(name:str=Query(...)):

    result=[e for e in enrollments if name.lower() in e["student"].lower()]

    return {"results":result}


@app.get("/enrollments/page")
def enrollment_page(page:int=1,limit:int=2):

    start=(page-1)*limit
    end=start+limit

    return {"data":enrollments[start:end]}
