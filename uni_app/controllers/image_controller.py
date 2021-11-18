from flask import Blueprint, request, redirect, abort, url_for, current_app
from pathlib import Path
from models.courses import Course
import boto3

course_images = Blueprint('course_images', __name__)

@course_images.route("/courses/<int:id>/image/", methods=["POST"])
def update_image(id):
    course=Course.query.get_or_404(id)
    if "image" in request.files:
        image = request.files["image"]
        if Path(image.filename).suffix != ".png":
            return abort(400, description="Invalid file type")
        
        bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
        bucket.upload_fileobj(image, course.image_filename)

        # image.save(f"static/{course.image_filename}")
        
        return redirect(url_for("courses.get_course", id=id))
    return abort(400, description="No image")

