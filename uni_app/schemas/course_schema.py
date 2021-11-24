from main import ma 
from models.courses import Course
from marshmallow_sqlalchemy import auto_field 
from marshmallow.validate import Length
from schemas.user_schema import UserSchema

class CourseSchema(ma.SQLAlchemyAutoSchema):
    course_id = auto_field(dump_only=True)
    course_name = auto_field(required=True, validate=Length(min=1))
    creator = ma.Nested("UserSchema")
    students = ma.Nested(
        "UserSchema", 
        only=("id", "name", "email",)
    )
    
    class Meta:
        model = Course
        load_instance = True

course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)
