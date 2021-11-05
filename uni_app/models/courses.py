from main import db

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
    def __init__(self, course_name):
        self.course_name = course_name

