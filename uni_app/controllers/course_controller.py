from flask import Blueprint, jsonify, request, render_template, redirect, url_for, current_app, abort
from main import db
from models.courses import Course
from schemas.course_schema import courses_schema, course_schema
from flask_login import login_required, current_user
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
    return render_template("course_index.html", page_data=data)

# The POST route endpoint
@courses.route("/courses/", methods=["POST"])
@login_required
def create_course():
    new_course=course_schema.load(request.form)
    new_course.creator = current_user
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

@courses.route("/courses/<int:id>/", methods=["POST"])
@login_required
def update_course(id):
    
    course = Course.query.filter_by(course_id=id)
    
    if current_user.id != course.first().creator_id:
        abort(403, "You do not have permission to alter this course")

    updated_fields = course_schema.dump(request.form)
    if updated_fields:
        course.update(updated_fields)
        db.session.commit()

    data = {
        "page_title": "Course Detail",
        "course": course_schema.dump(course.first())
    }
    return render_template("course_detail.html", page_data=data)

@courses.route("/courses/<int:id>/enrol/", methods=["POST"])
@login_required
def enrol_in_course(id):
    course = Course.query.filter_by(course_id=id).first()
    course.students.append(current_user)
    db.session.commit()
    return redirect(url_for('users.user_detail'))

@courses.route("/courses/<int:id>/drop/", methods=["POST"])
@login_required
def drop_course(id):
    course = Course.query.filter_by(course_id=id).first()
    course.students.remove(current_user)
    db.session.commit()
    return redirect(url_for('users.user_detail'))

@courses.route("/courses/<int:id>/delete/", methods=["POST"])
@login_required
def delete_course(id):
    course = Course.query.get_or_404(id)

    if current_user.id != course.creator_id:
        abort(403, "You do not have permission to alter this course")
    
    db.session.delete(course)
    db.session.commit()
    
    return redirect(url_for("courses.get_courses"))