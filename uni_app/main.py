import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

def create_app():
    
    # Creating the flask app object - this is the core of our app!
    app = Flask(__name__)

    app.config.from_object("config.app_config")

    # creating our database object! This allows us to use our ORM
    db = SQLAlchemy(app)

    # Our first model! 
    # This tells the ORM what tables should exist in the database
    # It also lets us retrieve info from those tables
    class Course(db.Model):
        # The tablename attribute specifies what the name of the table should be
        __tablename__ = "courses"

        # These attributes specify what columns the table should have
        course_id = db.Column(db.Integer, primary_key=True)
        course_name = db.Column(db.String(80), unique=True, nullable=False)

        # The init method lets us create a python object to insert as a new row
        def __init__(self,  course_name):
            self.course_name = course_name

        # The serialize property lets us turn our course objects into JSON easily
        # (we'll replace this with something more convenient later!)
        @property
        def serialize(self):
            return {
                "course_id": self.course_id,
                "course_name": self.course_name
            }

    # When the app first starts up, we tell our ORM to create any database
    # tables that don't already exist...
    db.create_all()

    # Then we can register our routes!

    # This one is just a placeholder for now, no CRUD here
    @app.route('/')
    def homepage():
        """
        The homepage route. 
        
        This will later contain information about what classes are available to enroll in.
        '/' is the address here, which means it will be available from our host domain. 
        During production this is localhost:5000 or 127.0.0.1:5000
        """
        return "Hello, world! Check this out!"

    # The GET routes endpoint
    @app.route("/courses/", methods=["GET"])
    def get_courses():
        # We use our model to query the database
        courses = Course.query.all()
        # and then serialize the resulting list of courses to return as JSON
        return jsonify([course.serialize for course in courses])

    # The POST route endpoint
    @app.route("/courses/", methods=["POST"])
    def create_course():
        # We initialise a new course instance based on the request data
        new_course=Course(request.json['course_name'])
        # add a row to the database with its info
        db.session.add(new_course)
        # commit the transaction
        db.session.commit()
        # serialise our new instance, and return as JSON
        return jsonify(new_course.serialize)

    # An endpoint to GET info about a specific course
    @app.route("/courses/<int:id>/", methods = ["GET"])
    def get_course(id):
        # Using the query.get_or_404 method here lets us automatically
        # return a 404 code if the indicated course doesn't exist
        course = Course.query.get_or_404(id)
        # but if it does exist, we just serialize it and return is as JSON
        return jsonify(course.serialize)

    # A PUT/PATCH route to update course info
    @app.route("/courses/<int:id>/", methods=["PUT", "PATCH"])
    def update_course(id):
        # To perform an update, we need a filtered list of queries
        # using query.get won't work here - just a quirk of Flask-SQLAlchemy's 
        # interface. It's set up this way so that you can update multiple records
        # at once if more than one matches your filter criteria
        course = Course.query.filter_by(course_id=id)
        # We hand a dictionary of the updated fields and their new values over
        # to the update method
        course.update(dict(course_name=request.json["course_name"]))
        # Gotta commit that transaction!
        db.session.commit()
        # since we are dealing with a filtered list of courses here, instead of
        # just a single object like we would have if we had been able to use the
        # query.get method, we have to grab the first item in the list before we
        # serialize it. This is the case even though there's only one item in this
        # list
        return jsonify(course.first().serialize)

    # Finally, we round out our CRUD resource with a DELETE method
    @app.route("/courses/<int:id>/", methods=["DELETE"])
    def delete_course(id):
        # Can't delete a course that doesn't exist, so get_or_404 here is correct
        course = Course.query.get_or_404(id)
        # delete the course and commit the transaction
        db.session.delete(course)
        db.session.commit()
        # We deleted the row in the database but we still have the python object
        # since we fetched it before we called session.delete, so we can 
        # serialize it and return it to the user to show them what they deleted!
        return jsonify(course.serialize)
        
    return app