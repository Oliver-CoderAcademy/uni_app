from flask import Blueprint, jsonify, request, render_template, redirect, url_for, current_app
from main import db
from models.courses import Course
from schemas.course_schema import courses_schema, course_schema
from flask_login import login_required
import boto3


courses = Blueprint('courses', __name__)

# This one is just a placeholder for now, no CRUD here
@courses.route('/')
def homepage():
    data = {
        "page_title": "Homepage"
    }
    return render_template("homepage.html", page_data=data)

# The GET routes endpoint
@courses.route("/courses/", methods=["GET"])
def get_courses():
    data = {
        "page_title": "Course Index",
        "courses": courses_schema.dump(Course.query.all())
    }
    print(data)
    return render_template("course_index.html", page_data=data)

# The POST route endpoint
@courses.route("/courses/", methods=["POST"])
@login_required
def create_course():
    new_course=course_schema.load(request.form)
    db.session.add(new_course)
    db.session.commit()
    return redirect(url_for("courses.get_courses"))

# An endpoint to GET info about a specific course
@courses.route("/courses/<int:id>/", methods = ["GET"])
def get_course(id):
    course = Course.query.get_or_404(id)
    
    s3_client=boto3.client('s3')
    bucket_name=current_app.config["AWS_S3_BUCKET"]
    image_url = s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': bucket_name,
            'Key': course.image_filename
        },
        ExpiresIn=100
    )
    
    data = {
        "page_title": "Course Detail",
        "course": course_schema.dump(course),
        "image": image_url
    }
    return render_template("course_detail.html", page_data=data)

# A PUT/PATCH route to update course info
@courses.route("/courses/<int:id>/", methods=["POST"])
@login_required
def update_course(id):
    
    course = Course.query.filter_by(course_id=id)
   
    updated_fields = course_schema.dump(request.form)
    if updated_fields:
        course.update(updated_fields)
        db.session.commit()

    data = {
        "page_title": "Course Detail",
        "course": course_schema.dump(course.first())
    }
    return render_template("course_detail.html", page_data=data)

# Finally, we round out our CRUD resource with a DELETE method
@courses.route("/courses/<int:id>/delete/", methods=["POST"])
@login_required
def delete_course(id):
    # Can't delete a course that doesn't exist, so get_or_404 here is correct
    course = Course.query.get_or_404(id)
    # delete the course and commit the transaction
    db.session.delete(course)
    db.session.commit()
    # We deleted the row in the database but we still have the python object
    # since we fetched it before we called session.delete, so we can 
    # serialize it and return it to the user to show them what they deleted!
    return redirect(url_for("courses.get_courses"))