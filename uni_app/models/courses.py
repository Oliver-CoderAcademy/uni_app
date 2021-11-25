from main import db
from models.users import User

enrolments = db.Table(
    'enrolments',
    db.Column('user_id', db.Integer, db.ForeignKey('flasklogin-users.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.course_id'), primary_key=True)
)

# Our first model! 
# This tells the ORM what tables should exist in the database
# It also lets us retrieve info from those tables
class Course(db.Model):
    # The tablename attribute specifies what the name of the table should be
    __tablename__ = "courses"

    # These attributes specify what columns the table should have
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(200), server_default="No Description Provided")
    cost = db.Column(db.Integer, nullable=False, server_default="0")

    creator_id = db.Column(db.Integer, db.ForeignKey('flasklogin-users.id'))

    students = db.relationship(
        User,
        secondary=enrolments,
        backref=db.backref('enrolled_courses'),
        lazy="joined"
    )

    @property
    def image_filename(self):
        return f"course_images/{self.course_id}.png"



