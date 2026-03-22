# FastAPI-Online-Course-Platform with the help of Innomatics research lab provided classes in my internship
## Project Overview
The project demonstrates the implementation of **FastAPI concepts from Day 1 to Day 6**, including CRUD operations, Pydantic validation, helper functions, search, sorting, pagination, and workflow APIs which are more used based on user needs.
## Features
* Course management system
* Course search by keyword
* Sorting courses by price or rating
* Pagination for course browsing
* Student enrollment workflow
* API validation using Pydantic models
* Error handling for invalid inputs
## Technologies Used
* Python
* FastAPI
* Pydantic
* Uvicorn
## API Endpoints
### Basic APIs
* `GET /` → Home route
* `GET /courses` → Get all courses
* `GET /courses/{course_id}` → Get course by ID
* `GET /courses/summary` → Course statistics
### Search & Filtering
* `GET /courses/search` → Search courses by keyword
* `GET /courses/sort` → Sort courses by price or rating
* `GET /courses/page` → Pagination
* `GET /courses/browse` → Combined filtering
### CRUD APIs
* `POST /courses` → Add new course
* `PUT /courses/{course_id}` → Update course
* `DELETE /courses/{course_id}` → Delete course
### Workflow APIs
* `POST /enroll` → Enroll student in a course
* `GET /enrollments` → View enrollments
* `GET /enrollments/search` → Search enrollments
* `GET /enrollments/page` → Enrollment pagination
## Running the Project
Install dependencies:
```
pip install fastapi uvicorn
```
Run the server:
```
uvicorn main:app --reload
```
Open Swagger UI:
```
http://127.0.0.1:8000/docs
```
