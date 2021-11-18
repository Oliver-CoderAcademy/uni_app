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
    description = db.Column(db.String(200), default="...")

    @property
    def image_filename(self):
        return f"course_images/{self.course_id}.png"

