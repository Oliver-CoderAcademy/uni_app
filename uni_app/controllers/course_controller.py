from flask import Blueprint, jsonify, request
from main import db
from models.courses import Course
from schemas.course_schema import courses_schema, course_schema

courses = Blueprint('courses', __name__)

# This one is just a placeholder for now, no CRUD here
@courses.route('/')
def homepage():
    """
    The homepage route. 
    
    This will later contain information about what classes are available to enroll in.
    '/' is the address here, which means it will be available from our host domain. 
    During production this is localhost:5000 or 127.0.0.1:5000
    """
    return "Hello, world! Check this out!"

# The GET routes endpoint
@courses.route("/courses/", methods=["GET"])
def get_courses():
    # We use our model to query the database
    courses = Course.query.all()
    # and then serialize the resulting list of courses to return as JSON
    return jsonify(courses_schema.dump(courses))

# The POST route endpoint
@courses.route("/courses/", methods=["POST"])
def create_course():
    new_course=course_schema.load(request.json)
    db.session.add(new_course)
    db.session.commit()
    return jsonify(course_schema.dump(new_course))

# An endpoint to GET info about a specific course
@courses.route("/courses/<int:id>/", methods = ["GET"])
def get_course(id):
    # Using the query.get_or_404 method here lets us automatically
    # return a 404 code if the indicated course doesn't exist
    course = Course.query.get_or_404(id)
    # but if it does exist, we just serialize it and return is as JSON
    return jsonify(course_schema.dump(course))

# A PUT/PATCH route to update course info
@courses.route("/courses/<int:id>/", methods=["PUT", "PATCH"])
def update_course(id):
    # To perform an update, we need a filtered list of queries
    # using query.get won't work here - just a quirk of Flask-SQLAlchemy's 
    # interface. It's set up this way so that you can update multiple records
    # at once if more than one matches your filter criteria
    course = Course.query.filter_by(course_id=id)
    # We hand a dictionary of the updated fields and their new values over
    # to the update method
    updated_fields = course_schema.dump(request.json)
    if updated_fields:
        course.update(updated_fields)
        # Gotta commit that transaction!
        db.session.commit()
    # since we are dealing with a filtered list of courses here, instead of
    # just a single object like we would have if we had been able to use the
    # query.get method, we have to grab the first item in the list before we
    # serialize it. This is the case even though there's only one item in this
    # list
    return jsonify(course_schema.dump(course.first()))

# Finally, we round out our CRUD resource with a DELETE method
@courses.route("/courses/<int:id>/", methods=["DELETE"])
def delete_course(id):
    # Can't delete a course that doesn't exist, so get_or_404 here is correct
    course = Course.query.get_or_404(id)
    # delete the course and commit the transaction
    db.session.delete(course)
    db.session.commit()
    # We deleted the row in the database but we still have the python object
    # since we fetched it before we called session.delete, so we can 
    # serialize it and return it to the user to show them what they deleted!
    return jsonify(course_schema.dump(course))