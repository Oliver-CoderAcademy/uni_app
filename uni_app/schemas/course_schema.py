from main import ma 
from models.courses import Course
from marshmallow_sqlalchemy import auto_field 
from marshmallow.validate import Length

class CourseSchema(ma.SQLAlchemyAutoSchema):
    course_id = auto_field(dump_only=True)
    course_name = auto_field(required=True, validate=Length(min=1))
    description = auto_field(validate=Length(min=1))

    class Meta:
        model = Course
        load_instance = True

course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)
